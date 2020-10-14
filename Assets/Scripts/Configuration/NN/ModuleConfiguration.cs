using System;
using Common;
using NN;

namespace Configuration.NN {
    [Serializable]
    public class ModuleConfiguration : ICopyable<ModuleConfiguration> {
        public ModuleLayerName layerName;

        public FloatParametersDict floatParameters = new FloatParametersDict();

        public IntParametersDict intParameters = new IntParametersDict();

        public void Deconstruct(out ModuleLayerName layerName, out FloatParametersDict floatParameters,
            out IntParametersDict intParameters) {
            layerName = this.layerName;
            floatParameters = this.floatParameters;
            intParameters = this.intParameters;
        }

        public ModuleConfiguration Copy() => new ModuleConfiguration
            {layerName = layerName, floatParameters = floatParameters, intParameters = intParameters};
    }
}