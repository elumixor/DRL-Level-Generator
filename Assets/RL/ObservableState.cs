namespace RL
{
    public abstract class ObservableState<TObservation> where TObservation : Vector
    {
        public abstract TObservation Observation { get; }
    }
}
