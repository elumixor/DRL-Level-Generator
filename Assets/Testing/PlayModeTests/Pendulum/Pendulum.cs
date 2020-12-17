using Common;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class Pendulum : MonoBehaviour
    {
        [SerializeField] Circle bob;
        [SerializeField] Transform lineRenderer;

        public float ConnectorLength {
            get => -bob.LocalPosition.y;
            set {
                bob.LocalPosition       = Vector2.down * value;
                lineRenderer.localScale = new Vector2(1, -value);
            }
        }

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
