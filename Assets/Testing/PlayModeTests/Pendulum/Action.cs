using Common;

namespace Testing.PlayModeTests.Pendulum
{
    public class Action : Vector
    {
        /// <inheritdoc/>
        public Action(bool doSwitch) : base(doSwitch ? 1f : -1f) { }

        public bool DoSwitch => values[0] >= 0;
        public const int SIZE = 2;
    }
}
