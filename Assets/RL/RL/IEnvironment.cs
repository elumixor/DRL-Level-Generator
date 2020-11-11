namespace RL.RL
{
    public interface IEnvironment<TState, in TAction>
    {
        /// <summary> Called at the beginning of the episode to reset everything to new episode </summary>
        TState ResetEnvironment();

        /// <summary>
        ///     Perform the agent's step in the environment, return the reward and the flag if the environment is finished
        /// </summary>
        /// <param name="action"> Action that the agent has decided to take </param>
        /// <returns>
        ///     A 3-tuple with new state, reward from taking the action, either true if reached a terminal state, or false otherwise
        /// </returns>
        (TState newState, float reward, bool isDone) Step(TAction action);
    }
}
