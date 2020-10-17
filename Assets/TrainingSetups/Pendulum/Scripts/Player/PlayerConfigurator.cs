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
        void ApplyConfiguration() {
            ApplyStructuralConfiguration();
        }

        void ApplyStructuralConfiguration() {
            connectorConfigurator.ApplyConfiguration(structuralConfiguration);
            bobConfigurator.ApplyConfiguration(structuralConfiguration);
        }

        void Update() {
            if (watchForChanges) ApplyConfiguration();
        }
    }
}