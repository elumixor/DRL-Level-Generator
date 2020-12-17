using Common;
using Common.ByteConversions;
using NN;
using NN.Configuration;
using RemoteComputation.Models;

namespace RL
{
    public abstract class LocalInferenceNN : IRemoteModel, IByteAssignable, IActor
    {
        protected Module nn;

        /// <inheritdoc/>
        public int Id { get; protected set; }

        /// <inheritdoc/>
        public abstract ModelType ModelType { get; }

        /// <inheritdoc/>
        public virtual Vector GetAction(Vector state) => nn.Forward(state).ArgMax();

        /// <inheritdoc/>
        public virtual void AssignFromBytes(ByteReader reader)
        {
            Id = reader.ReadInt();
            nn = reader.Read<Sequential>();
            nn.LoadStateDict(reader.Read<StateDict>());
        }
    }
}
