using System;
using Common;
using NN;

namespace Configuration.NN {
    [Serializable]
    public class ModuleConfiguration : ICopyable<ModuleConfiguration> {
        [Serializable]
        public enum ModuleConfigurationParameterFloat {
            None
        }

        [Serializable]
        public enum ModuleConfigurationParameterInt {
            None,
            InputSize,
            OutputSize,
        }

        [Serializable]
        public class IntParametersDict : SerializableDictionary<ModuleConfigurationParameterInt, int> { }

        [Serializable]
        public class FloatParametersDict : SerializableDictionary<ModuleConfigurationParameterFloat, float> { }
        
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