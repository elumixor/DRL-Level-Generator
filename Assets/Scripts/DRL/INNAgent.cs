using Configuration.NN;
using NN;

namespace DRL {
    /// <summary>
    ///     Agent with NN
    /// </summary>
    public interface INNAgent {
        Module NN { get; }
        void InitializeNN(Layout layout);
    }
}