using Common;
using NaughtyAttributes;
using RL.RLBehaviours;
using UnityEditor;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts
{
    [SelectionBase, ExecuteInEditMode]
    public class Environment : EnvironmentInstance<State, int, Agent>
    {
        // Referenced components
        [SerializeField, BoxGroup("References")] Circle enemy;               // will receive position from it
        [SerializeField, BoxGroup("References")] Transform playerAttachment; // used to get/set position and get/set current angle
        [SerializeField, BoxGroup("References")] Circle playerBob;           // used to set according to radius

        // Parameters to set
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter startPositionY;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter enemyPositionX;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter enemyPositionY;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter connectorLength;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter bobRadius;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter enemyRadius;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter maxAngle;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter startingAngle;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter startAngularDirection;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter verticalSpeed;
        [SerializeField, BoxGroup("Parameters")] EnvironmentParameter angularSpeed;

        // Rewards
        [SerializeField, BoxGroup("Rewards")] float stepReward;
        [SerializeField, BoxGroup("Rewards")] float collidedReward;
        [SerializeField, BoxGroup("Rewards")] float passedReward;

        [SerializeField, BoxGroup("Background")] Transform outer;
        [SerializeField, BoxGroup("Background")] Transform inner;
        [SerializeField, BoxGroup("Background"), Range(0, 1)] float borderSize = 1f;
        [SerializeField, BoxGroup("Background"), Range(0, 2)] float padding = 1f;

        float angularSpeedSampled;
        float verticalSpeedSampled;
        float maxAngleSampled;

        float angularVelocity;
        float passedY;
        float angle;

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
            angularSpeedSampled  = angularSpeed;
            verticalSpeedSampled = verticalSpeed;
            maxAngleSampled      = maxAngle;

            // Set local position as we will have several instances at once, each will be offset
            playerAttachment.localPosition    = Vector3.up      * startPositionY;
            playerAttachment.localEulerAngles = Vector3.forward * (angle = startingAngle);
            playerBob.LocalPosition           = Vector3.down    * connectorLength;
            enemy.LocalPosition               = new Vector2(enemyPositionX, enemyPositionY);

            playerBob.Radius = bobRadius;
            enemy.Radius     = enemyRadius;

            angularVelocity = angularSpeedSampled * startAngularDirection;

            passedY = enemy.LocalPosition.y + enemy.Radius + playerBob.Radius;

            ResizeBackground();

            return CurrentState;
        }

        /// <inheritdoc/>
        public override (State newState, float reward, bool isDone) Step(int action)
        {
            // Update vertically
            var newPosition = playerAttachment.localPosition + Vector3.up * verticalSpeedSampled;

            var changed = false;

            if (action > 0) {
                angularVelocity *= -1f;
                changed         =  true;
            }

            // Updated swing stuff
            angle += angularVelocity;

            if (Mathf.Abs(angle) >= maxAngleSampled) {
                angle = 2 * Mathf.Sign(angle) * maxAngleSampled - angle;
                if (!changed) angularVelocity *= -1f;
            }

            playerAttachment.localEulerAngles = Vector3.forward * angle;

            var collided = enemy.Intersects(playerBob);
            var passed = playerBob.Position.y < passedY && newPosition.y >= passedY;
            var done = collided || passed;
            var reward = collided ? collidedReward : passed ? passedReward : stepReward;

            playerAttachment.localPosition = newPosition;

            return (CurrentState, reward, done);
        }

        void Update()
        {
            if (EditorApplication.isPlaying) return;

            startPositionY.Max = Mathf.Min(startPositionY.Max, enemy.Position.y - enemy.Radius);

            ResetEnvironment();

            ResizeBackground();
        }

        void ResizeBackground()
        {
            if (outer == null || inner == null) return;

            var playerY = playerAttachment.localPosition.y;
            var height = enemy.LocalPosition.y + enemyRadius + 2 * bobRadius + 2 * connectorLength - playerY;
            var width = Mathf.Max(Mathf.Sin(maxAngle * Mathf.Deg2Rad) * connectorLength + bobRadius, Mathf.Abs(enemy.LocalPosition.x) + enemyRadius) * 2;

            var center = height * .5f - (-playerY + connectorLength + bobRadius);

            var outerPosition = outer.localPosition;
            var innerPosition = inner.localPosition;

            outerPosition.y = center;
            innerPosition.y = center;

            outer.localPosition = outerPosition;
            inner.localPosition = innerPosition;

            outer.localScale = new Vector3(width + padding         + borderSize, height + padding + borderSize);
            inner.localScale = new Vector3(width + padding, height + padding);
        }
    }
}
