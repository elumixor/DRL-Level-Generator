using System;
using Common;
using RL.NN;

namespace RL
{
    public class DQNEpisodeEvaluator : IEpisodeEvaluator<IState, int, float>, INNAgent
    {
        Module dqn;
        float epsilon;

        /// <inheritdoc/>
        public void InitializeNN(Module nn) { dqn = nn; }

        /// <inheritdoc/>
        public void SetParameters(StateDict stateDict) => dqn.LoadStateDict(stateDict);

        /// <inheritdoc/>
        public int GetAction(IState state)
        {
            var qValues = dqn.Forward(state.ToVector());
            return qValues.SampleEpsilonGreedy(epsilon);
        }

        /// <inheritdoc/>
        public void Train(Action onceTrainingCompleted) { throw new NotImplementedException(); }

        /// <inheritdoc/>
        public void EvaluateDifficulty(Action<float> onceEvaluated) { throw new NotImplementedException(); }
    }
}
