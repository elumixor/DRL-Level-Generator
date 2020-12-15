using Common;

namespace RL
{
    public interface IEnvironment
    {
        Vector Reset(Vector generatedData); // needs to be differentiable to generatedInitialState
        (Vector nextState, float reward, bool done) Transition(Vector state, Vector action); // needs to be differentiable to state
    }
}
