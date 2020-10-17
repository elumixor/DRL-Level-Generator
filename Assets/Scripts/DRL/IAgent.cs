namespace DRL {
    public interface IAgent<TAction, TState> {
        void Initialize(IEnvironment<TAction, TState> environment);
        void OnEpisodeStarted();
        TAction GetAction(TState state);
        void SaveTransition(Transition<TAction, TState> transition);
        void OnEpisodeFinished();
        void OnEpochFinished();
    }
}