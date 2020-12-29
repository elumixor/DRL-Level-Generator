using Common;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class Pendulum : MonoBehaviour
    {
        [SerializeField] CircleBehaviour bob;
        [SerializeField] Transform lineRenderer;

        public float ConnectorLength {
            get => -bob.transform.localPosition.y;
            set {
                bob.transform.localPosition = Vector2.down * value;
                lineRenderer.localScale     = new Vector2(1, -value);
            }
        }

        public float BobRadius {
            get => bob.circle.radius;
            set {
                bob.circle.radius = value;
                bob.OnValidate();
            }
        }

        public float Angle {
            get => transform.localEulerAngles.z;
            set => transform.localEulerAngles = Vector3.forward * value;
        }

        public CircleBehaviour Bob => bob;
    }
}
