using UnityEngine;

namespace Common
{
    public class Circle : MonoBehaviour
    {
        [SerializeField] float radius = 1;

        public Vector2 Position {
            get => transform.position;
            set => transform.position = value;
        }

        public Vector2 LocalPosition {
            get => transform.localPosition;
            set => transform.localPosition = value;
        }
        public float Radius {
            get => radius;
            set => transform.localScale = Vector3.one * (2 * (radius = value));
        }

        public bool Intersects(Circle other) => (Position - other.Position).magnitude - radius - other.radius <= 0;

        void Reset()
        {
            radius = 1f;
            OnValidate();
        }

        void OnValidate()
        {
            radius               = Mathf.Max(radius, 0);
            transform.localScale = Vector3.one * (2 * radius);
        }
    }
}
