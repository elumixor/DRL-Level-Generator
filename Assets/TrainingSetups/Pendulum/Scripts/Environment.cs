using Common;
using Editor.PropertyDrawers;
using NaughtyAttributes;
using RL.RLBehaviours;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts
{
    [SelectionBase]
    public class Environment : EnvironmentInstance<State, int, Agent>
    {
        // Referenced components
        [SerializeField, BoxGroup("References")] Circle enemy;               // will receive position from it
        [SerializeField, BoxGroup("References")] Transform playerAttachment; // used to get/set position and get/set current angle
        [SerializeField, BoxGroup("References")] Circle playerBob;           // used to set according to radius

        // Parameters to set
        [SerializeField, BoxGroup("Parameters"), Range(0, 10)] float connectorLength;
        [SerializeField, BoxGroup("Parameters"), Range(0, 10)] float bobRadius;
        [SerializeField, BoxGroup("Parameters"), Range(0, 10)] float enemyRadius;
        [SerializeField, BoxGroup("Parameters"), Range(0, 90)] float maxAngle;
        [SerializeField, BoxGroup("Parameters"), AbsRangeDependant(nameof(maxAngle))] float startingAngle;
        [SerializeField, BoxGroup("Parameters"), PlusMinus(PositiveLabel = "To Right", NegativeLabel = "To Left")] float startAngularDirection;
        [SerializeField, BoxGroup("Parameters"), Range(0, 10)] float verticalSpeed;
        [SerializeField, BoxGroup("Parameters"), Range(0, 10)] float angularSpeed;

        // Rewards
        [SerializeField, BoxGroup("Rewards")] float stepReward;
        [SerializeField, BoxGroup("Rewards")] float collidedReward;
        [SerializeField, BoxGroup("Rewards")] float passedReward;

        [SerializeField, BoxGroup("Background")] Transform outer;
        [SerializeField, BoxGroup("Background")] Transform inner;
        [SerializeField, BoxGroup("Background"), Range(0, 1)] float borderSize = 1f;
        [SerializeField, BoxGroup("Background"), Range(0, 2)] float padding = 1f;

        float angularVelocity;
        float passedY;

        Vector3 ClosestEnemyRelativePosition => enemy.Position - playerBob.Position;

        State CurrentState =>
                new State {
                        position                     = playerAttachment.localPosition.y,
                        angle                        = playerAttachment.localEulerAngles.z,
                        angularVelocity              = angularVelocity,
                        closestEnemyRelativePosition = ClosestEnemyRelativePosition,
                };

        /// <inheritdoc/>
        public override State ResetEnvironment()
        {
            // Set local position as we will have several instances at once, each will be offset
            playerAttachment.localPosition    = Vector3.zero;
            playerAttachment.localEulerAngles = Vector3.forward * startingAngle;
            playerBob.LocalPosition           = Vector3.down    * connectorLength;
            playerBob.Radius                  = bobRadius;
            enemy.Radius                      = enemyRadius;

            angularVelocity = angularSpeed * startAngularDirection;

            passedY = enemy.Position.y + enemy.Radius + playerBob.Radius;

            return CurrentState;
        }

        /// <inheritdoc/>
        public override (State newState, float reward, bool isDone) Step(int action)
        {
            // Update vertically
            playerAttachment.localPosition += Vector3.up * verticalSpeed;

            // Updated swing stuff
            var currentAngle = playerAttachment.localEulerAngles.z;
            currentAngle += angularVelocity;

            if (Mathf.Abs(currentAngle) > maxAngle) currentAngle = 2 * maxAngle - currentAngle;

            playerAttachment.localEulerAngles = Vector3.forward * currentAngle;

            var collided = enemy.Intersects(playerBob);
            var passed = playerBob.Position.y > passedY;
            var done = collided || passed;
            var reward = collided ? collidedReward : passed ? passedReward : stepReward;

            return (CurrentState, reward, done);
        }

        void OnValidate()
        {
            startingAngle = Mathf.Clamp(startingAngle, -maxAngle, maxAngle);

            if (outer != null && inner != null) {
                var height = enemy.LocalPosition.y + enemyRadius + 2 * bobRadius + 2 * connectorLength - playerAttachment.localPosition.y;
                var width = Mathf.Max(Mathf.Sin(maxAngle * Mathf.Deg2Rad) * connectorLength + bobRadius, Mathf.Abs(enemy.LocalPosition.x) + enemyRadius) * 2;

                outer.localScale = new Vector3(width + padding         + borderSize, height + padding + borderSize);
                inner.localScale = new Vector3(width + padding, height + padding);
            }

            ResetEnvironment();
        }
    }
}
