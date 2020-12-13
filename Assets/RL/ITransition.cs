namespace RL.RL
{
    public interface ITransition<out TState, out TAction>
    {
        TState Vector { get; }
        TAction Action { get; }
        float Reward { get; }
        TState NextState { get; }
    }
}
