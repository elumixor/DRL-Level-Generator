using System;
using NaughtyAttributes;
using Player.Configuration;
using Player.Configuration.Configurators;
using UnityEngine;

namespace Player {
    /// <summary>
    /// Master class for configuring the player
    /// </summary>
    [ExecuteInEditMode]
    public class PlayerConfigurator : MonoBehaviour {
        [SerializeField] private StructuralConfiguration structuralConfiguration;
        [SerializeField] private BehaviouralConfiguration behaviouralConfiguration;
        
        [SerializeField, Foldout("Components")] private BobConfigurator bobConfigurator;
        [SerializeField, Foldout("Components")] private ConnectorConfigurator connectorConfigurator;
        [SerializeField] private bool watchForChanges = true;

        // Expose configurations
        public BehaviouralConfiguration BehaviouralConfiguration => behaviouralConfiguration;
        public StructuralConfiguration StructuralConfiguration => structuralConfiguration;

        /// <summary>
        /// Applies the structural and behavioural configuration to the player
        /// </summary>
        [Button]
        private void ApplyConfiguration() {
            ApplyStructuralConfiguration();
        }

        private void ApplyStructuralConfiguration() {
            connectorConfigurator.ApplyConfiguration(structuralConfiguration);
            bobConfigurator.ApplyConfiguration(structuralConfiguration);
        }

        private void Update() {
            if (watchForChanges) ApplyConfiguration();
        }
    }
}