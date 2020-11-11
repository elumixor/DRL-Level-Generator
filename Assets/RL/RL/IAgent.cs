namespace RL.RL
{
    public interface IAgent<in TState, out TAction>
    {
        TAction GetAction(TState state);
    }
}
