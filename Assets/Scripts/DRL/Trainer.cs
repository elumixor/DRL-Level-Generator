namespace DRL {
    /// <summary>
    /// Connects training environment and an agent to control the general training.
    /// Designed asynchronously around Unity's update. Listens to <see cref="IEnvironment{TAction,TObservation}.Stepped"/> event to control training. 
    /// </summary>
    public class Trainer<TAction, TState> {
        readonly IEnvironment<TAction, TState> environment;
        readonly IAgent<TAction, TState> agent;
        readonly int epochs;
        readonly int episodesPerEpoch;
        readonly int maximumEpisodeLength;

        TState previousState;
        TAction previousAction;
        float previousReward;

        // Track current training data
        int epoch;
        int episode;
        int step;
        float episodeReward;

        /// <summary>
        /// Fires when the episode is finished, with the total accumulated reward in this episode
        /// </summary>
        public event System.Action<float> EpisodeFinished = delegate { };

        /// <summary>
        /// Create a new trainer instance
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

            agent.Initialize(environment);
        }

        /// <summary>
        /// Starts the training for the specified number of epochs, episodes and steps
        /// </summary>
        public void StartTraining() {
            epoch = 0;
            episode = 0;

            environment.Stepped += OnEnvironmentStepped;
            environment.IsActive = true;
            StartNewEpisode();
        }

        void OnEnvironmentStepped(TState state) {
            if (step != 0)
                agent.SaveTransition(new Transition<TAction, TState>(previousState, previousAction, previousReward, state));

            var action = agent.GetAction(state);

            var (reward, isDone) = environment.Step(action);

            previousAction = action;
            previousState = state;
            previousReward = reward;

            step++;
            episodeReward += reward;

            if (isDone || step >= maximumEpisodeLength) OnEpisodeFinished();
        }

        void StartNewEpisode() {
            step = 0;
            episodeReward = 0;

            environment.ResetEnvironment();
            agent.OnEpisodeStarted();
        }

        void OnEpisodeFinished() {
            episode++;
            agent.OnEpisodeFinished();

            EpisodeFinished(episodeReward);

            if (episode >= episodesPerEpoch) {
                epoch++;
                agent.OnEpochFinished();
            }

            if (epoch < epochs) StartNewEpisode();
            else OnTrainingFinished();
        }

        void OnTrainingFinished() {
            environment.IsActive = false;
            environment.Stepped -= OnEnvironmentStepped;
        }
    }
}