namespace RL
{
    public interface IEnvironment<in TGeneratedData, TState, in TAction>
    {
        TState ResetEnvironment(TGeneratedData generatedData); // needs to be differentiable to generatedInitialState
        (TState nextState, float reward, bool done) Transition(TState state, TAction action); // needs to be differentiable to state
    }

    public interface IEnvironment : IEnvironment<Vector, Vector, Vector> { }
}
