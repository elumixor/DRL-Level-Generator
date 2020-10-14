using System;
using System.Collections.Generic;
using Configuration.AlgorithmConfigurations;
using NaughtyAttributes;
using UnityEngine;

namespace Configuration {
    [CreateAssetMenu(fileName = "Setup.configuration.asset", menuName = "Training Setup Configuration", order = 0)]
    public partial class Configuration : ScriptableObject {
        [SerializeField] AlgorithmNames algorithm;

        [SerializeField] ConfigurationVPG configurationVPG;
        [SerializeField] ConfigurationA2C configurationA2C;

        public float discounting;
        public AlgorithmConfiguration AlgorithmConfiguration {
            get {
                switch (algorithm) {
                    case AlgorithmNames.VPG:
                        return configurationVPG;
                    case AlgorithmNames.A2C:
                        return configurationA2C;
                    default:
                        throw new ArgumentOutOfRangeException();
                }
            }
        }
    }
}