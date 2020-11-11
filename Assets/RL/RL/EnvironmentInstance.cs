using System.Collections.Generic;

namespace RL.RL
{
    public class EnvironmentInstance<TState, TAction>
    {
        readonly IEnvironment<TState, TAction> environment;
        readonly IAgent<TState, TAction> agent;

        // Keep in memory the last state received from the environment to feed to the agent to perform inference
        TState state;

        // We'll use this to cut off long episodes
        public int maximumEpisodeLength;

        public EnvironmentInstance(IEnvironment<TState, TAction> environment, IAgent<TState, TAction> agent)
        {
            this.environment = environment;
            this.agent       = agent;
            Episode          = new List<(TState state, TAction action, float reward, TState nextState)>();
        }

        // First, training instance will prepare self for the new episode
        public void StartNewEpisode()
        {
            if (Episode.Count > 0) Episode = new List<(TState state, TAction action, float reward, TState nextState)>();

            state  = environment.ResetEnvironment();
            IsDone = maximumEpisodeLength <= 0;
        }

        // Performs an environmental step when this command is received
        public void Step()
        {
            var action = agent.GetAction(state);

            var (nextState, reward, isDone) = environment.Step(action);

            Episode.Add((state, action, reward, nextState));

            state  = nextState;
            IsDone = isDone || Episode.Count >= maximumEpisodeLength;
        }

        // When true, the episode has finished and the samples are gathered
        public bool IsDone { get; private set; }

        // Collect the episode and creates the new one
        public List<(TState state, TAction action, float reward, TState nextState)> Episode { get; set; }
    }
}
