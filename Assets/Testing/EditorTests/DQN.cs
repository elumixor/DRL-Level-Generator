using RemoteComputation.Models;
using RL;

namespace Testing.EditorTests
{
    class DQN : LocalInferenceNN
    {
        /// <inheritdoc/>
        public override ModelType ModelType { get; } = ModelType.DQN;

        /// <inheritdoc/>
        public override string ToString() => "DQN:\n" + nn;
    }
}
