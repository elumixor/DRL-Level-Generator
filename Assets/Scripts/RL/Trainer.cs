using System;

namespace RL {
    /// <summary>
    ///     Connects training environment and an agent to control the general training.
    ///     Designed asynchronously around Unity's update. Listens to <see cref="IEnvironment{TAction,TObservation}.Stepped" /> event to control
    ///     training.
    /// </summary>
    public class Trainer<TAction, TState> {
        readonly IAgent<TAction, TState> agent;
        readonly IEnvironment<TAction, TState> environment;
        readonly int episodesPerEpoch;
        readonly int epochs;
        readonly int maximumEpisodeLength;
        TState currentState;
        int episodeIndex;

        int epochIndex;

        TAction previousAction;
        float previousReward;
        int stateIndex;

        /// <summary>
        ///     Create a new trainer instance
        /// </summary>
        /// <param name="environment">Training environment</param>
        /// <param name="agent">Agent to be used while training</param>
        /// <param name="epochs">Number of epochs to train. Each epoch consists of several episodes</param>
        /// <param name="episodesPerEpoch">Number of episodes within an epoch</param>
        /// <param name="maximumEpisodeLength">Maximum number of steps in an episode. Used to cutoff the long (possibly infinite) episodes</param>
        public Trainer(IEnvironment<TAction, TState> environment, IAgent<TAction, TState> agent, int epochs = 100, int episodesPerEpoch = 1,
                       int maximumEpisodeLength = -1) {
            this.environment = environment;
            this.agent = agent;
            this.epochs = epochs;
            this.episodesPerEpoch = episodesPerEpoch;
            this.maximumEpisodeLength = maximumEpisodeLength;

            agent.OnEnvironmentCreated(environment);
        }

        public event Action TrainingFinished = delegate { };

        /// <summary>
        ///     Starts the training for the specified number of epochs, episodes and steps
        /// </summary>
        public void StartTraining() {
            epochIndex = 0;
            episodeIndex = 0;
            stateIndex = 0;

            StartNewEpisode();
        }

        // Perform a step in the environment
        public void Step() {
            var action = agent.GetAction(currentState);
            var (newState, reward, isDone) = environment.Step(action);
            agent.OnTransition(currentState, action, reward, newState);
            currentState = newState;

            stateIndex++;

            if (isDone || stateIndex >= maximumEpisodeLength) OnEpisodeFinished();
        }

        void StartNewEpisode() {
            stateIndex = 0;

            currentState = environment.ResetEnvironment();
            agent.OnEpisodeStarted();
        }

        void OnEpisodeFinished() {
            episodeIndex++;
            agent.OnEpisodeFinished();

            if (episodeIndex >= episodesPerEpoch) {
                epochIndex++;
                episodeIndex = 0;
                agent.OnEpochFinished();
            }

            if (epochs < 1 || epochIndex < epochs) StartNewEpisode();
            else OnTrainingFinished();
        }

        void OnTrainingFinished() => TrainingFinished();
    }
}