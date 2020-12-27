using Common;

namespace RL
{
    public interface IActor<in TState, out TAction>
            where TState : Vector
            where TAction : Vector
    {
        TAction GetAction(TState state);
    }

    public interface IActor : IActor<Vector, Vector> { }
}
