using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    [ExecuteInEditMode]
    public class EnvironmentVisualizer : MonoBehaviour
    {
        [SerializeField] Transform inner;
        [SerializeField] Transform outer;

        [SerializeField] float border;

        public float width;
        public float height;

        void Update()
        {
            if (inner != null) inner.localScale = new Vector3(width, height);
            if (outer != null) outer.localScale = new Vector3(width + border * 2, height + border * 2);
        }
    }
}
