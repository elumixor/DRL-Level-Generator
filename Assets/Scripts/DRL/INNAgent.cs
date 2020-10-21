using Configuration.NN;
using NN;

namespace DRL {
    /// <summary>
    ///     Agent with NN
    /// </summary>
    public interface INNAgent {
        void InitializeNN(Layout layout, StateDict stateDict);
    }
}