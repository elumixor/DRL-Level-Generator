using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;
using NN;

namespace Configuration.NN {
    [Serializable]
    public class ModuleConfiguration : ICopyable<ModuleConfiguration>, IByteConvertible {
        [Serializable]
        public enum ModuleConfigurationParameterFloat {
            None,
        }

        [Serializable]
        public enum ModuleConfigurationParameterInt {
            None,
            InputSize,
            OutputSize,
        }

        public FloatParametersDict floatParameters = new FloatParametersDict();

        public IntParametersDict intParameters = new IntParametersDict();

        public ModuleLayerName layerName;

        public IEnumerable<byte> ToBytes() => layerName.ToString().ToBytes().ConcatMany(floatParameters.ToBytes(), intParameters.ToBytes());

        public ModuleConfiguration Copy() => new ModuleConfiguration
            {layerName = layerName, floatParameters = floatParameters, intParameters = intParameters};

        public void Deconstruct(out ModuleLayerName layerName, out FloatParametersDict floatParameters,
                                out IntParametersDict intParameters) {
            layerName = this.layerName;
            floatParameters = this.floatParameters;
            intParameters = this.intParameters;
        }

        [Serializable]
        public class IntParametersDict : SerializableDictionary<ModuleConfigurationParameterInt, int>, IByteConvertible {
            public IEnumerable<byte> ToBytes() =>
                Count.ToBytes().Concat(this.SelectMany(kvp => kvp.Key.ToString().ToBytes().Concat(kvp.Value.ToBytes())));
        }

        [Serializable]
        public class FloatParametersDict : SerializableDictionary<ModuleConfigurationParameterFloat, float>, IByteConvertible {
            public IEnumerable<byte> ToBytes() =>
                Count.ToBytes().Concat(this.SelectMany(kvp => kvp.Key.ToString().ToBytes().Concat(kvp.Value.ToBytes())));
        }
    }
}