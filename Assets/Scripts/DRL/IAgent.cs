namespace DRL {
    public interface IAgent<TAction, in TState> {
        void OnEnvironmentCreated(IEnvironment<TAction, TState> environment);
        void OnEpisodeStarted();
        TAction GetAction(TState state);
        void OnTransition(TState previousState, TAction action, float reward, TState nextState);
        void OnEpisodeFinished();
        void OnEpochFinished();
    }
}