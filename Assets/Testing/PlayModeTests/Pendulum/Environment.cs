using System.Linq;
using Common;
using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class Environment : IEnvironment<GeneratedData, State, Action>
    {
        const float MAX_ANGLE = 60f;
        const float VERTICAL_SPEED = 1f;
        const float ANGULAR_SPEED = 10f;

        Circle[] enemies;
        float bobRadius;
        float connectorLength;
        float passPoint;

        public State ResetEnvironment(GeneratedData generatedData)
        {
            var enemiesCount = Mathf.RoundToInt(generatedData.EnemiesCount);
            enemies = new Circle[enemiesCount];

            bobRadius       = generatedData.BobRadius;
            connectorLength = generatedData.ConnectorLength;

            var top = float.NegativeInfinity;

            for (var i = 0; i < enemiesCount; i++) {
                var (position, radius) = generatedData.GetEnemy(i);
                var circle = new Circle(position, radius);
                enemies[i] = circle;

                var enemyTop = position.y + radius;
                if (enemyTop > top) top = enemyTop;
            }

            passPoint = top + connectorLength + bobRadius;

            return new State(0, generatedData.Angle, generatedData.AngularDirection);
        }

        public (State nextState, float reward, bool done) Transition(State state, Action action)
        {
            var (verticalPosition, angle, angularDirection) = state.Observation;
            var doSwitch = action.DoSwitch;
            var deltaTime = action.DeltaTime;

            if (doSwitch) angularDirection *= -1;
            angle += angularDirection * deltaTime * ANGULAR_SPEED;

            if (angle >= MAX_ANGLE) {
                angle            =  2 * MAX_ANGLE - angle;
                angularDirection *= -1;
            } else if (angle <= -MAX_ANGLE) {
                angle            =  -2 * MAX_ANGLE - angle;
                angularDirection *= -1;
            }

            var nextState = new State(verticalPosition + VERTICAL_SPEED * deltaTime, angle, angularDirection);

            var passed = verticalPosition >= passPoint;

            var y = verticalPosition - Mathf.Cos(angle * Mathf.Deg2Rad) * connectorLength;
            var x = Mathf.Sin(angle * Mathf.Deg2Rad) * connectorLength;

            var bobPosition = new Vector2(x, y);

            var bobCircle = new Circle(bobPosition, bobRadius);

            var collided = enemies.Any(enemy => enemy.Intersects(bobCircle));

            var done = collided || passed;

            var reward = passed ? 10f : collided ? 0f : VERTICAL_SPEED;
            return (nextState, reward, done);
        }
    }
}
