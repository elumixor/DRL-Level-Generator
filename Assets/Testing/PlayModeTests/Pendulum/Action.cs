using Common;

namespace Testing.PlayModeTests.Pendulum {
    public class Action : Vector {
        public bool DoSwitch => values[0] >= 0;
    }
}