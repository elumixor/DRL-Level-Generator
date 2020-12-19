using System.Linq;
using Common;
using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class Environment : MonoBehaviour, IEnvironment<GeneratedData, State, Action>, IStateRenderer<State>
    {
        [SerializeField] Pendulum pendulum;
        [SerializeField] EnvironmentVisualizer visualizer;
        [SerializeField] float maxAngle = 60;
        [SerializeField] GameObject enemyPrefab;

        Circle[] enemies;
        float passPoint;
        const float VERTICAL_SPEED = 1f;

        public State ResetEnvironment(GeneratedData generatedData)
        {
            // Cleanup previously positioned enemies
            if (enemies != null)
                foreach (var enemy in enemies)
                    Destroy(enemy.gameObject);

            var connectorLength = generatedData.ConnectorLength;
            var bobRadius = generatedData.BobRadius;

            pendulum.ConnectorLength = connectorLength;
            pendulum.BobRadius       = bobRadius;
            pendulum.Angle           = generatedData.Angle;
            var angularDirection = generatedData.AngularDirection;
            pendulum.transform.localPosition = Vector3.zero;

            var enemiesCount = Mathf.RoundToInt(generatedData.EnemiesCount);
            enemies = new Circle[enemiesCount];

            var top = float.NegativeInfinity;
            var left = 0f;

            for (var i = 0; i < enemiesCount; i++) {
                var enemy = Instantiate(enemyPrefab, transform, true);
                var circle = enemy.AddComponent<Circle>();

                var (position, radius) = generatedData.GetEnemy(i);
                circle.LocalPosition   = position;
                circle.Radius          = radius;

                var enemyTop = position.y        + radius;
                var enemyLeft = position.x.Abs() + radius;

                if (enemyTop  > top) top   = enemyTop;
                if (enemyLeft > left) left = enemyLeft;

                enemies[i] = circle;
            }

            var playerSize = connectorLength + bobRadius;
            passPoint = top + playerSize;

            if (visualizer != null) {
                var height = passPoint + playerSize;

                visualizer.height = height;
                visualizer.width  = left * 2;

                visualizer.transform.localPosition = Vector3.up * (passPoint / 2);
            }

            return new State(0, pendulum.Angle, angularDirection);
        }

        public (State nextState, float reward, bool done) Transition(State state, Action action)
        {
            var (verticalPosition, angle, angularDirection) = state;
            var doSwitch = action.DoSwitch;
            var deltaTime = action.DeltaTime;

            if (doSwitch) angularDirection *= -VERTICAL_SPEED;
            angle += angularDirection * deltaTime;

            if (angle >= maxAngle) {
                angle            =  2 * maxAngle - angle;
                angularDirection *= -VERTICAL_SPEED;
            } else if (angle <= -maxAngle) {
                angle            =  -2 * maxAngle - angle;
                angularDirection *= -VERTICAL_SPEED;
            }

            var nextState = new State(verticalPosition + VERTICAL_SPEED * deltaTime, angle, angularDirection);

            var bob = pendulum.Bob;

            var passed = verticalPosition >= passPoint;
            var collided = enemies.Any(enemy => enemy.Intersects(bob));
            // Debug.Log(verticalPosition + " " + passPoint + " " + passed + " " + collided);

            var done = collided || passed;

            var reward = passed ? 10f : collided ? 0f : VERTICAL_SPEED;
            return (nextState, reward, done);
        }

        public void RenderState(State state)
        {
            var (verticalPosition, angle, _) = state;
            pendulum.transform.localPosition = Vector3.up * verticalPosition;
            pendulum.Angle                   = angle;
        }
    }
}
