namespace DRL {
    public interface IAgent<TAction, TObservation> {
        void Initialize(IEnvironment<TAction, TObservation> environment);
        void OnEpisodeStarted();
        TAction GetAction(TObservation observation);
        void SaveTransition(Transition<TAction, TObservation> transition);
        void OnEpisodeFinished();
        void OnEpochFinished();
    }
}