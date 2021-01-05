using System.Linq;
using Common.RandomValues;
using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum.Generators
{
    public class PlacedGenerator : MonoBehaviour, IGenerator<GeneratedData>
    {
        [SerializeField] float connectorLength;
        [SerializeField] float bobRadius;
        [SerializeField] float maxAngle;
        GeneratedData.CircleConfiguration[] enemies;

        public void FindEnemies()
        {
            enemies = GameObject.FindGameObjectsWithTag("Enemy")
                                .Select(enemy => {
                                     var t = enemy.transform;
                                     var localPosition = t.localPosition;
                                     return new GeneratedData.CircleConfiguration(localPosition.x, localPosition.y, t.localScale.x * 0.5f);
                                 })
                                .ToArray();
        }

        /// <inheritdoc/>
        public GeneratedData Generate(float difficulty, float randomSeed = 0)
        {
            // Randomize starting angle
            var angle = UniformValue.Get(-maxAngle, maxAngle);

            // Randomize starting angular direction
            var angularDirection = EitherValue.Get(1, -1);

            return new GeneratedData(connectorLength, bobRadius, angle, angularDirection, 5f, enemies.Length, enemies);
        }
    }
}
