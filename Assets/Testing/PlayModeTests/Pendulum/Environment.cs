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

        GameObject[] enemiesObjects;
        Circle[] enemies;

        float passPoint;
        const float VERTICAL_SPEED = 1f;

        bool shouldReset;
        GeneratedData generatedData;

        public State ResetEnvironment(GeneratedData generatedData)
        {
            shouldReset        = true;
            this.generatedData = generatedData;
            var enemiesCount = Mathf.RoundToInt(generatedData.EnemiesCount);

            enemies = new Circle[enemiesCount];

            for (var i = 0; i < enemiesCount; i++) {
                var (position, radius) = generatedData.GetEnemy(i);
                var circle = new Circle(position, radius);
                enemies[i] = circle;
            }

            return new State(0, generatedData.Angle, generatedData.AngularDirection);
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
            var collided = enemies.Any(enemy => enemy.Intersects(bob.circle));
            // Debug.Log(verticalPosition + " " + passPoint + " " + passed + " " + collided);

            var done = collided || passed;

            var reward = passed ? 10f : collided ? 0f : VERTICAL_SPEED;
            return (nextState, reward, done);
        }

        public void RenderState(State state)
        {
            if (shouldReset) {
                // Cleanup previously positioned enemies
                if (enemiesObjects != null)
                    foreach (var enemy in enemiesObjects)
                        Destroy(enemy);

                var connectorLength = generatedData.ConnectorLength;
                var bobRadius = generatedData.BobRadius;

                pendulum.ConnectorLength         = connectorLength;
                pendulum.BobRadius               = bobRadius;
                pendulum.Angle                   = generatedData.Angle;
                pendulum.transform.localPosition = Vector3.zero;

                var enemiesCount = Mathf.RoundToInt(generatedData.EnemiesCount);
                enemiesObjects = new GameObject[enemiesCount];

                var top = float.NegativeInfinity;
                var left = 0f;

                for (var i = 0; i < enemiesCount; i++) {
                    var enemy = Instantiate(enemyPrefab, transform, true);
                    var circle = enemy.AddComponent<CircleBehaviour>();
                    circle.circle = enemies[i];

                    var (position, radius)         = generatedData.GetEnemy(i);
                    circle.OnValidate();

                    var enemyTop = position.y        + radius;
                    var enemyLeft = position.x.Abs() + radius;

                    if (enemyTop  > top) top   = enemyTop;
                    if (enemyLeft > left) left = enemyLeft;

                    enemiesObjects[i] = enemy;
                }

                var playerSize = connectorLength + bobRadius;
                passPoint = top + playerSize;

                if (visualizer != null) {
                    var height = passPoint + playerSize;

                    visualizer.height = height;
                    visualizer.width  = left * 2;

                    visualizer.transform.localPosition = Vector3.up * (passPoint / 2);
                }

                shouldReset = false;
            }

            var (verticalPosition, angle, _) = state;
            pendulum.transform.localPosition = Vector3.up * verticalPosition;
            pendulum.Angle                   = angle;
        }
    }
}
