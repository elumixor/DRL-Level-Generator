using System.Collections.Generic;

namespace NN {
    public abstract class Module {
        public abstract float[] Forward(float[] input);
        public virtual void SetParameter(ModuleParameterName parameterName, Tensor value) { }

        public virtual void LoadStateDict(StateDict stateDict) {
            foreach (var kvp in stateDict.selfParameters)
                SetParameter(kvp.Key, kvp.Value);
        }

        public virtual StateDict GetStateDict() => new StateDict(new Dictionary<ModuleParameterName, Tensor>(),
                                                                 new List<(int[] path, (ModuleParameterName name, Tensor value) parameter)
                                                                 >());
    }
}