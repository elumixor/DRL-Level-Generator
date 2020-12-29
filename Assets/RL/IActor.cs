namespace RL
{
    public interface IActor<in TObservation, out TAction> where TObservation : Vector
                                                          where TAction : Vector
    {
        TAction GetAction(TObservation obs);
    }

    public interface IActor : IActor<Vector, Vector> { }
}
