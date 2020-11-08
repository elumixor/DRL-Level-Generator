namespace NN
{
    /// <summary> Agent with NN </summary>
    public interface INNAgent
    {
        void InitializeNN(Module nn);
        void SetParameters(StateDict stateDict);
    }
}
