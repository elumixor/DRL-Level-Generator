using System;

namespace RL
{
    /// A DQN agent, with DQN on a remote backend, that can train, and can also evaluate then, using DQN
    public interface IEpisodeEvaluator<TState, TAction, TDifficulty>
    {
        /// Needs to do (immediate: on front) inference to actually get actions and act in the environment
        TAction GetAction(TState state);

        /// Needs to be trained on backend
        void Train(Action onceTrainingCompleted);

        /// Needs to evaluate the difficulty (remotely)
        void EvaluateDifficulty(Action<TDifficulty> onceEvaluated);
    }
}
