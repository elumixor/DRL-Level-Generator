using Common;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.Other
{
    [ExecuteInEditMode, RequireComponent(typeof(LineRenderer))]
    public class ConnectingLine : MonoBehaviour
    {
        [SerializeField] Circle bob;

        readonly Vector3[] positions = {new Vector3(0, 0), new Vector3(0, 0)};

        LineRenderer lineRenderer;

        void Start() { lineRenderer = GetComponent<LineRenderer>(); }

        void Update()
        {
            if (bob == null) return;

            positions[0] = transform.parent.position;
            positions[1] = bob.Position;

            lineRenderer.SetPositions(positions);
            lineRenderer.positionCount = 2;
        }
    }
}
