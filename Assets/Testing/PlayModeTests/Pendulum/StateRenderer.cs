using Common;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class StateRenderer : MonoBehaviour, IStateRenderer<State, GeneratedData>
    {
        [SerializeField] Pendulum pendulum;
        [SerializeField] EnvironmentVisualizer visualizer;
        [SerializeField] GameObject enemyPrefab;

        GameObject[] enemiesObjects;

        float passPoint;
        float connectorLength;
        float bobRadius;

        public void Setup(GeneratedData generatedData)
        {
            if (enemiesObjects != null)
                foreach (var enemy in enemiesObjects)
                    Destroy(enemy);

            // Cleanup previously positioned enemies
            connectorLength = generatedData.ConnectorLength;
            bobRadius       = generatedData.BobRadius;

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

                var (position, radius) = generatedData.GetEnemy(i);

                circle.circle.radius           = radius;
                circle.transform.localPosition = position;

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
        }

        public void RenderState(State state)
        {
            var (verticalPosition, angle, _) = state.Observation;
            pendulum.transform.localPosition = Vector3.up * verticalPosition;
            pendulum.Angle                   = angle;
        }
    }
}
