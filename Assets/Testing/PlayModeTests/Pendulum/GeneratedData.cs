using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class GeneratedData : Vector
    {
        public readonly struct CircleConfiguration
        {
            public readonly Vector2 position;
            public readonly float radius;

            public CircleConfiguration(float x, float y, float radius)
            {
                position    = new Vector2(x, y);
                this.radius = radius;
            }

            public void Deconstruct(out Vector2 position, out float radius)
            {
                position = this.position;
                radius   = this.radius;
            }
        }

        public float ConnectorLength => values[0];
        public float BobRadius => values[1];
        public float Angle => values[2];
        public float AngularDirection => values[3];
        public float VerticalSize => values[4];
        public int EnemiesCount => Mathf.RoundToInt(values[5]);

        const int ENEMIES_OFFSET = 6;

        public CircleConfiguration GetEnemy(int i) =>
                new CircleConfiguration(values[ENEMIES_OFFSET + i * 3],
                                        values[ENEMIES_OFFSET + i * 3 + 1],
                                        values[ENEMIES_OFFSET + i * 3 + 2]);

        public GeneratedData
        (float connectorLength,
         float bobRadius,
         float angle,
         float angularDirection,
         float verticalSize,
         int enemiesCount,
         params CircleConfiguration[] enemies) : base(new float[ENEMIES_OFFSET + enemiesCount * 3])
        {
            values[0] = connectorLength;
            values[1] = bobRadius;
            values[2] = angle;
            values[3] = angularDirection;
            values[4] = verticalSize;
            values[5] = enemiesCount;

            for (var i = 0; i < enemiesCount; i++) {
                var (position, radius)             = enemies[i];
                values[ENEMIES_OFFSET + i * 3]     = position.x;
                values[ENEMIES_OFFSET + i * 3 + 1] = position.y;
                values[ENEMIES_OFFSET + i * 3 + 2] = radius;
            }
        }
    }
}
