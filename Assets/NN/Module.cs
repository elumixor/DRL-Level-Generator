using System.Collections.Generic;
using NN.Configuration;

namespace NN
{
    public abstract class Module
    {
        public virtual StateDict StateDict =>
                new StateDict(new Dictionary<ModuleParameterName, Tensor>(),
                              new List<(int[] path, (ModuleParameterName name, Tensor value) parameter)>());

        public abstract IEnumerable<float> Forward(IEnumerable<float> input);
        public virtual void SetParameter(ModuleParameterName parameterName, Tensor value) { }

        public virtual void LoadStateDict(StateDict stateDict)
        {
            foreach (var kvp in stateDict.selfParameters) SetParameter(kvp.Key, kvp.Value);
        }
    }
}
