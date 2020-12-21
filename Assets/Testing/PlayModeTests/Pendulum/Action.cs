using Common;
using RL;

namespace Testing.PlayModeTests.Pendulum
{
    public class Action : Vector, IDeltaTimedAction
    {
        /// <inheritdoc/>
        public Action(bool doSwitch, float deltaTime = 1f) : base(doSwitch ? 1f : 0f, deltaTime) { }

        public bool DoSwitch => values[0] >= 0.5f;
        public const int SIZE = 2;

        public float DeltaTime => values[1];
    }
}
