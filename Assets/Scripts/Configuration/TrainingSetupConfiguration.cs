using System;
using Configuration.AlgorithmConfigurations;
using UnityEngine;

namespace Configuration {
    [CreateAssetMenu(fileName = "Training Setup.asset", menuName = "Training Setup Configuration", order = 0)]
    public partial class TrainingSetupConfiguration : ScriptableObject {
        [SerializeField] Algorithm algorithm;

        [SerializeField] ConfigurationVPG configurationVPG;
        [SerializeField] ConfigurationA2C configurationA2C;

        // Hyperparameters
        public float discounting;
        
        // Configuration of selected Algorithm
        public AlgorithmConfiguration AlgorithmConfiguration {
            get {
                switch (algorithm) {
                    case Algorithm.VPG:
                        return configurationVPG;
                    case Algorithm.A2C:
                        return configurationA2C;
                    default:
                        throw new ArgumentOutOfRangeException();
                }
            }
        }
    }
}