using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum.Generators
{
    public abstract class PendulumGenerator : MonoBehaviour, IGenerator<GeneratedData>
    {
        /// <inheritdoc/>
        public abstract GeneratedData Generate(float difficulty, float randomSeed = 0);
    }
}
