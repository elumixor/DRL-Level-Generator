﻿using NaughtyAttributes;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.Player.Configuration.Configurators {
    [RequireComponent(typeof(LineRenderer))]
    public class ConnectorConfigurator : MonoBehaviour {
        [SerializeField, Range(2, 100)] int smoothness;

        float length;

        public void ApplyConfiguration(StructuralConfiguration structuralConfiguration) {
            transform.localScale = new Vector3(1, structuralConfiguration.connectorLength, -1);
        }

        [Button]
        void UpdateLineRenderer() {
            var positions = new Vector3[smoothness];

            for (var i = 0; i < smoothness; i++)
                positions[i] = (float) i / (smoothness - 1) * Vector3.down;

            var lineRenderer = GetComponent<LineRenderer>();
            lineRenderer.SetPositions(positions);
            lineRenderer.positionCount = smoothness;
        }
    }
}