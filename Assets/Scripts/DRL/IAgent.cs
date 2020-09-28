namespace DRL {
    public interface IAgent<TAction, TObservation> {
        void Initialize(IEnvironment<TAction, TObservation> environment);
        void OnEpisodeStarted();
        TAction GetAction(TObservation observation);
        void SaveStep(TObservation previousObservation, TAction action, float reward);
        void OnEpisodeFinished();
        void OnEpochFinished();
    }
}