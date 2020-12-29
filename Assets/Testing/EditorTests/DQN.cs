using Common;
using RemoteComputation.Models;
using RL;

namespace Testing.EditorTests
{
    class DQN : LocalInferenceNN<Vector, Vector>
    {
        /// <inheritdoc/>
        public override ModelType ModelType { get; } = ModelType.DQN;

        /// <inheritdoc/>
        public override Vector GetAction(Vector obs) => nn.Forward(obs).ArgMax();

        /// <inheritdoc/>
        public override string ToString() => "DQN:\n" + nn;
    }
}
