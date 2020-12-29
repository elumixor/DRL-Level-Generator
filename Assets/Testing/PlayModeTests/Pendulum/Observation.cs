using RL;

namespace Testing.PlayModeTests.Pendulum
{
    public class Observation : Vector
    {
        public const int SIZE = 3;

        public Observation
                (float verticalPosition, float angle, float angularDirection) : base(verticalPosition, angle, angularDirection) { }

        public float VerticalPosition => values[0];
        public float Angle => values[1];
        public float AngularDirection => values[2];

        /* Helpers */

        public void Deconstruct(out float verticalPosition, out float angle, out float angularDirection)
        {
            verticalPosition = VerticalPosition;
            angle            = Angle;
            angularDirection = AngularDirection;
        }
    }
}
