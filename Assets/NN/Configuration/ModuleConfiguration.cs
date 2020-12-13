using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;

namespace NN.Configuration
{
    [Serializable]
    public class ModuleConfiguration : IByteConvertible
    {
        [Serializable]
        public enum ModuleConfigurationParameterFloat
        {
            None,
        }

        [Serializable]
        public enum ModuleConfigurationParameterInt
        {
            None,
            InputSize,
            OutputSize,
        }

        public FloatParametersDict floatParameters;

        public readonly IntParametersDict intParameters;

        public readonly ModuleLayerName layerName;

        public ModuleConfiguration(ModuleLayerName layerName, IntParametersDict intParameters, FloatParametersDict floatParameters)
        {
            this.layerName       = layerName;
            this.intParameters   = intParameters;
            this.floatParameters = floatParameters;
        }

        public ModuleConfiguration(ModuleConfiguration other) : this(other.layerName, other.intParameters, other.floatParameters) { }

        public IEnumerable<byte> Bytes => layerName.ToString().ToBytes().ConcatMany(intParameters.Bytes, floatParameters.Bytes);

        public void Deconstruct(out ModuleLayerName layerName, out FloatParametersDict floatParameters, out IntParametersDict intParameters)
        {
            layerName       = this.layerName;
            floatParameters = this.floatParameters;
            intParameters   = this.intParameters;
        }

        [Serializable]
        public class IntParametersDict : SerializableDictionary<ModuleConfigurationParameterInt, int>, IByteConvertible
        {
            public IEnumerable<byte> Bytes {
                get {
                    var selected = this.Where(kvp => kvp.Key != ModuleConfigurationParameterInt.None).ToArray();

                    return selected.Length.ToBytes()
                                   .Concat(selected.SelectMany(kvp => kvp.Key.ToString().ToBytes().Concat(kvp.Value.ToBytes())));
                }
            }
        }

        [Serializable]
        public class FloatParametersDict : SerializableDictionary<ModuleConfigurationParameterFloat, float>, IByteConvertible
        {
            public IEnumerable<byte> Bytes {
                get {
                    var selected = this.Where(kvp => kvp.Key != ModuleConfigurationParameterFloat.None).ToArray();

                    return selected.Length.ToBytes()
                                   .Concat(selected.SelectMany(kvp => kvp.Key.ToString().ToBytes().Concat(kvp.Value.ToBytes())));
                }
            }

            public static readonly FloatParametersDict Empty = new FloatParametersDict();
        }
    }
}
