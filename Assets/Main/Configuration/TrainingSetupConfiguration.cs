using System;
using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using Configuration.AlgorithmConfigurations;
using UnityEngine;

namespace Configuration
{
    [CreateAssetMenu(fileName = "Training Setup.asset", menuName = "Training Setup Configuration", order = 0)]
    public partial class TrainingSetupConfiguration : ScriptableObject, IByteConvertible
    {
        [NonSerialized] public int actionSize;
        [SerializeField] Algorithm algorithm;
        [SerializeField] ConfigurationA2C configurationA2C;

        [SerializeField] ConfigurationVPG configurationVPG;
        [NonSerialized] public int stateSize;

        // Configuration of selected Algorithm
        public AlgorithmConfiguration AlgorithmConfiguration {
            get {
                switch (algorithm) {
                    case Algorithm.VPG: return configurationVPG;
                    case Algorithm.A2C: return configurationA2C;
                    default:            throw new ArgumentOutOfRangeException();
                }
            }
        }

        public IEnumerable<byte> ToBytes()
        {
            var algorithmBytes = algorithm.ToString().ToBytes();
            var configurationBytes = AlgorithmConfiguration.ToBytes();
            var actionSizeBytes = actionSize.ToBytes();
            var stateSizeBytes = stateSize.ToBytes();
            return algorithmBytes.ConcatMany(configurationBytes, actionSizeBytes, stateSizeBytes);
        }
    }
}
