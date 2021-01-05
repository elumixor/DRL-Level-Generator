using Common;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum.StateRenderers
{
    public class PlacedRenderer : MonoBehaviour, IStateRenderer<State, GeneratedData>
    {
        Pendulum pendulum;
        EnvironmentVisualizer visualizer;

        float passPoint;
        float connectorLength;
        float bobRadius;

        public void Setup(GeneratedData generatedData)
        {
            // Cleanup previously positioned enemies
            connectorLength = generatedData.ConnectorLength;
            bobRadius       = generatedData.BobRadius;

            pendulum   = FindObjectOfType<Pendulum>();
            visualizer = FindObjectOfType<EnvironmentVisualizer>();

            pendulum.ConnectorLength         = connectorLength;
            pendulum.BobRadius               = bobRadius;
            pendulum.Angle                   = generatedData.Angle;
            pendulum.transform.localPosition = Vector3.zero;

            var enemiesCount = Mathf.RoundToInt(generatedData.EnemiesCount);

            var top = float.NegativeInfinity;
            var left = connectorLength + bobRadius;

            for (var i = 0; i < enemiesCount; i++) {
                var (position, radius) = generatedData.GetEnemy(i);

                var enemyTop = position.y        + radius;
                var enemyLeft = position.x.Abs() + radius;

                if (enemyTop  > top) top   = enemyTop;
                if (enemyLeft > left) left = enemyLeft;
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
