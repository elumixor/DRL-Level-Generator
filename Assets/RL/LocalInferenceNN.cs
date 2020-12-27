using Common;
using Common.ByteConversions;
using NN;
using NN.Configuration;
using RemoteComputation.Models;

namespace RL
{
    public abstract class LocalInferenceNN<TState, TAction> : IRemoteModel, IByteAssignable, IActor<TState, TAction>
            where TState : Vector
            where TAction : Vector
    {
        protected Module nn;

        /// <inheritdoc/>
        public int Id { get; protected set; }

        /// <inheritdoc/>
        public abstract ModelType ModelType { get; }

        /// <inheritdoc/>
        public abstract TAction GetAction(TState state);

        /// <inheritdoc/>
        public virtual void AssignFromBytes(ByteReader reader)
        {
            Id = reader.ReadInt();
            nn = reader.Read<Sequential>();
            nn.LoadStateDict(reader.Read<StateDict>());
        }
    }
}
