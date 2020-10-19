using System.Collections.Generic;

namespace NN {
    public readonly struct StateDict {
        public readonly IDictionary<ModuleParameterName, float[]> selfParameters;
        public readonly IEnumerable<(int childIndex, StateDict stateDict)> childParameters;

        public StateDict(byte[] bytes, int startIndex) {
            selfParameters = new Dictionary<ModuleParameterName, float[]>();
            childParameters = new (int, StateDict)[10];
        }

        public StateDict(IDictionary<ModuleParameterName, float[]> selfParameters, IEnumerable<(int, StateDict)> childParameters) {
            this.selfParameters = selfParameters;
            this.childParameters = childParameters;
        }

        public void Deconstruct(out IDictionary<ModuleParameterName, float[]> selfParameters,
                                out IEnumerable<(int childIndex, StateDict stateDict)> childParameters) {
            selfParameters = this.selfParameters;
            childParameters = this.childParameters;
        }
    }
}