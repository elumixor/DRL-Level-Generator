using Serialization;

namespace TrainingSetups.LeftRight.Scripts
{
    public class Action
    {
        public static readonly Action Left = new Action(0);
        public static readonly Action Right = new Action(1);

        Action(float x) => X = x;

        public Action(int value) : this(value == 0 ? 0f : 1f) { }

        [Structural] public float X { get; }
    }
}
