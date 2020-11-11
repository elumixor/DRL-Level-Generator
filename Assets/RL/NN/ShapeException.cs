using System.Runtime.Serialization;

namespace RL.NN
{
    public class ShapeException : SerializationException
    {
        public ShapeException(string message = "Shapes do not match") : base(message) { }
    }
}
