using System.Linq;
using Common;
using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class Environment : MonoBehaviour, IEnvironment<GeneratedData, State, Action>, IStateRenderer<State>
    {
        [SerializeField] Pendulum pendulum;
        [SerializeField] float maxAngle = 60;
        [SerializeField] GameObject enemyPrefab;

        Circle[] enemies;

        public State ResetEnvironment(GeneratedData generatedData)
        {
            // Cleanup previously positioned enemies
            if (enemies != null)
                foreach (var enemy in enemies)
                    Destroy(enemy.gameObject);

            pendulum.ConnectorLength = generatedData.ConnectorLength;
            pendulum.BobRadius       = generatedData.BobRadius;
            pendulum.Angle           = generatedData.Angle;
            var angularDirection = generatedData.AngularDirection;
            pendulum.transform.localPosition = Vector3.zero;

            var enemiesCount = Mathf.RoundToInt(generatedData.EnemiesCount);
            enemies = new Circle[enemiesCount];

            for (var i = 0; i < enemiesCount; i++) {
                var enemy = Instantiate(enemyPrefab, transform, true);
                var circle = enemy.AddComponent<Circle>();

                var (position, radius) = generatedData.GetEnemy(i);
                circle.LocalPosition   = position;
                circle.Radius          = radius;

                enemies[i] = circle;
            }

            return new State(0, pendulum.Angle, angularDirection);
        }

        public (State nextState, float reward, bool done) Transition(State state, Action action)
        {
            var (verticalPosition, angle, angularDirection) = state;
            var doSwitch = action.DoSwitch;

            if (doSwitch) angularDirection *= -1f;
            angle += angularDirection;

            if (angle >= maxAngle) {
                angle            =  2 * maxAngle - angle;
                angularDirection *= -1f;
            } else if (angle <= -maxAngle) {
                angle            =  -2 * maxAngle - angle;
                angularDirection *= -1f;
            }

            var nextState = new State(verticalPosition + 1f, angle, angularDirection);

            var bob = pendulum.Bob;
            var done = enemies.Any(enemy => enemy.Intersects(bob));

            var reward = done ? 0f : 1f;
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
