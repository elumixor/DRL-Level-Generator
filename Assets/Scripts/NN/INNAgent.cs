using Configuration.NN;

namespace NN
{
    /// <summary> Agent with NN </summary>
    public interface INNAgent
    {
        void ConstructNN(Layout layout);
        void SetParameters(StateDict stateDict);
    }
}
