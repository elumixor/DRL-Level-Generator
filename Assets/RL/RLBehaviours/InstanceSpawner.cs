using System;
using System.Collections.Generic;
using RL.Exceptions;
using UnityEngine;
using Object = UnityEngine.Object;

namespace RL.RLBehaviours
{
    [Serializable]
    public class InstanceSpawner
    {
        public MonoBehaviour environment;

        public int count;

        public int rows;
        public float columnSpacing;
        public float rowSpacing;

        public IEnumerable<TEnvironmentInstance> Spawn<TEnvironmentInstance>()
                where TEnvironmentInstance : MonoBehaviour
        {
            var environmentInstance = environment.GetComponent<TEnvironmentInstance>();

            if (environmentInstance == null) throw new BaseException("Environment is not of a type " + typeof(TEnvironmentInstance));

            yield return environmentInstance;

            var columns = Mathf.CeilToInt((float) count / rows);

            var basePosition = environment.transform.position;
            var created = 1;

            for (var i = 0; i < columns; i++)
            for (var j = i == 0 ? 1 : 0; j < rows; j++) {
                if (created >= count) yield break;

                var offset = basePosition + new Vector3(columnSpacing * j, 0, rowSpacing * i);

                yield return Object.Instantiate(environmentInstance, basePosition + offset, Quaternion.identity);

                created++;
            }
        }

        public void DrawGizmosGrid()
        {
            var columns = Mathf.CeilToInt((float) count / rows);

            var xMin = -columnSpacing / 2;
            var yMin = -rowSpacing    / 2;

            var xMax = -columnSpacing * (columns + 1) / 2;
            var yMax = -rowSpacing    * (rows    + 1) / 2;

            // Draw column lines
            for (var i = 0; i < columns + 1; i++) {
                var x = xMin + columnSpacing * i;

                Gizmos.DrawLine(new Vector3(x, yMin), new Vector3(x, yMax));
            }

            // Draw column lines
            for (var i = 0; i < rows + 1; i++) {
                var y = yMin + rowSpacing * i;

                Gizmos.DrawLine(new Vector3(xMin, 0, y), new Vector3(xMax, 0, y));
            }
        }
    }
}
