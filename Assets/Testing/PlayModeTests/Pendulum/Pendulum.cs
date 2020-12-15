using Common;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class Pendulum : MonoBehaviour
    {
        [SerializeField] Circle bob;

        public float ConnectorLength { get; set; }

        public float BobRadius {
            get => bob.Radius;
            set => bob.Radius = value;
        }

        public float Angle {
            get => transform.localEulerAngles.z;
            set => transform.localEulerAngles = Vector3.forward * value;
        }

        public Circle Bob => bob;
    }
}
