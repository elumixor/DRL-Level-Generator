using System;
using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using RL.Configuration.AlgorithmConfigurations;
using UnityEngine;

namespace RL.Configuration
{
    [CreateAssetMenu(fileName = "Training Configuration.asset", menuName = "Training Configuration", order = 0)]
    public class TrainingConfiguration : ScriptableObject
    {
        [SerializeField] Algorithm algorithm;
        [SerializeField] ConfigurationA2C configurationA2C;
        [SerializeField] ConfigurationVPG configurationVPG;

        // These are retrieved from the selected State and Action types
        [NonSerialized] public int stateSize;
        public int actionSize;

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
            var configurationBytes = AlgorithmConfiguration.ToBytes(stateSize, actionSize);
            var actionSizeBytes = actionSize.ToBytes();
            var stateSizeBytes = stateSize.ToBytes();
            return algorithmBytes.ConcatMany(configurationBytes, actionSizeBytes, stateSizeBytes);
        }
    }
}
