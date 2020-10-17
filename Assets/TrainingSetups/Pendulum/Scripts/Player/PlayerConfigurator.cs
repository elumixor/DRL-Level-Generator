using NaughtyAttributes;
using TrainingSetups.Pendulum.Scripts.Player.Configuration;
using TrainingSetups.Pendulum.Scripts.Player.Configuration.Configurators;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.Player {
    /// <summary>
    /// Master class for configuring the player
    /// </summary>
    [ExecuteInEditMode]
    public class PlayerConfigurator : MonoBehaviour {
        [SerializeField] StructuralConfiguration structuralConfiguration;
        [SerializeField] BehaviouralConfiguration behaviouralConfiguration;

        [SerializeField, Foldout("Components")] BobConfigurator bobConfigurator;
        [SerializeField, Foldout("Components")] ConnectorConfigurator connectorConfigurator;
        [SerializeField] bool watchForChanges = true;

        // Expose configurations
        public BehaviouralConfiguration BehaviouralConfiguration => behaviouralConfiguration;
        public StructuralConfiguration StructuralConfiguration => structuralConfiguration;

        /// <summary>
        /// Applies the structural and behavioural configuration to the player
        /// </summary>
        [Button]
        void ApplyConfiguration() { ApplyStructuralConfiguration(); }

        void ApplyStructuralConfiguration() {
            connectorConfigurator.ApplyConfiguration(structuralConfiguration);
            bobConfigurator.ApplyConfiguration(structuralConfiguration);
        }

        void Update() {
            if (watchForChanges) ApplyConfiguration();
        }
    }
}