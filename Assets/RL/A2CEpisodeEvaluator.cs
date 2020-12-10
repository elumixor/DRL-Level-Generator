using System;
using Common;
using RemoteComputation;
using RL.NN;

namespace RL
{
    public class A2CEpisodeEvaluator : IEpisodeEvaluator<IState, int, float>, INNAgent
    {
        Module actor;

        readonly RemoteModel remoteModel;

        public int GetAction(IState state) => actor.Forward(state.ToVector()).Softmax().Sample();

        /// <inheritdoc/>
        public void InitializeNN(Module nn) { actor = nn; }

        /// <inheritdoc/>
        public void SetParameters(StateDict stateDict) => actor.LoadStateDict(stateDict);

        /// <inheritdoc/>
        public void Train(Action onceTrainingCompleted) { throw new NotImplementedException(); }

        /// <inheritdoc/>
        public void EvaluateDifficulty(Action<float> onceEvaluated) { throw new NotImplementedException(); }
    }
}
