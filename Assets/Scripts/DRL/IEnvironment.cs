namespace DRL {
    public interface IEnvironment<in TAction, out TState> {
        /// <summary>
        /// Called at the beginning of the episode to reset everything to new episode
        /// </summary>
        void ResetEnvironment();

        /// <summary>
        /// Perform the agent's step in the environment, return the reward and the flag if the environment is finished 
        /// </summary>
        /// <param name="action"></param>
        /// <returns></returns>
        (float reward, bool isDone) Step(TAction action);

        /// <summary>
        /// Emit this event when the training step should be executed, i.e. in your Update() function after the observation is received
        /// </summary>
        event System.Action<TState> Stepped;

        /// <summary>
        /// Is set in the trainer. Used to notify the environment that the environment is up and running.
        /// Check for this flag in your Update() function and skip the training logic if the flag turned off  
        /// </summary>
        bool IsActive { set; }
    }
}