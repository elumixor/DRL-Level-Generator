namespace RL {
    public interface IEnvironment<in TAction, TState> {
        /// <summary>
        ///     Called at the beginning of the episode to reset everything to new episode
        /// </summary>
        TState ResetEnvironment();

        /// <summary>
        ///     Perform the agent's step in the environment, return the reward and the flag if the environment is finished
        /// </summary>
        /// <param name="action"></param>
        /// <returns></returns>
        (TState newState, float reward, bool isDone) Step(TAction action);
    }
}