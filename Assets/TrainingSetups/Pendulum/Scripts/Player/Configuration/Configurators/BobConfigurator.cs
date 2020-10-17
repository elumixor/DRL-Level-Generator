using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.Player.Configuration.Configurators {
    public class BobConfigurator : MonoBehaviour {
        public void ApplyConfiguration(StructuralConfiguration structuralConfiguration) {
            var t = transform;

            t.localScale = structuralConfiguration.bobSize * Vector3.one;
            t.localPosition = Vector3.down * structuralConfiguration.connectorLength;
        }
    }
}