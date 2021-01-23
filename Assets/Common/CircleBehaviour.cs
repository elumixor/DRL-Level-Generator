using UnityEngine;

namespace Common
{
    public class CircleBehaviour : MonoBehaviour
    {
        public Circle circle;

        void Reset()
        {
            circle.radius = 1f;
            OnValidate();
        }

        public void OnValidate()
        {
            if (circle == null) return;

            circle.radius        = Mathf.Max(circle.radius, 0);
            transform.localScale = Vector3.one * (2 * circle.radius);
        }
    }
}
