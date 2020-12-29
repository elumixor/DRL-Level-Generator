using Common;
using Common.ByteConversions;
using NN;
using NN.Configuration;
using RemoteComputation.Models;

namespace RL
{
    public abstract class LocalInferenceNN<TObservation, TAction> : IRemoteModel, IByteAssignable, IActor<TObservation, TAction>
            where TObservation : Vector
            where TAction : Vector
    {
        protected Module nn;

        /// <inheritdoc/>
        public int Id { get; protected set; }

        /// <inheritdoc/>
        public abstract ModelType ModelType { get; }

        /// <inheritdoc/>
        public abstract TAction GetAction(TObservation obs);

        /// <inheritdoc/>
        public virtual void AssignFromBytes(ByteReader reader)
        {
            Id = reader.ReadInt();
            nn = reader.Read<Sequential>();
            nn.LoadStateDict(reader.Read<StateDict>());
        }
    }
}
