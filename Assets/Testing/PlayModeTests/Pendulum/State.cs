using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using RL;

namespace Testing.PlayModeTests.Pendulum
{
    public class State : ObservableState<Observation>, IByteConvertible
    {
        readonly Circle[] enemies;

        public State
                (float verticalPosition, float angle, float angularDirection) =>
                Observation = new Observation(verticalPosition, angle, angularDirection);

        /// <inheritdoc/>
        public override Observation Observation { get; }

        /// <inheritdoc/>
        public IEnumerable<byte> Bytes => Observation.Bytes;
    }
}
