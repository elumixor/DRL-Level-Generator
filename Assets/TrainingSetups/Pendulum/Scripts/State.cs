using System.Collections;
using System.Collections.Generic;
using RL.Serialization;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts
{
    public class State : IEnumerable<float>
    {
        [Structural] public float position;
        [Structural] public float angle;
        [Structural] public float angularVelocity;
        [Structural] public Vector2 closestEnemyRelativePosition;

        public IEnumerator<float> GetEnumerator()
        {
            yield return position;
            yield return angle;

            yield return angularVelocity;

            yield return closestEnemyRelativePosition.x;
            yield return closestEnemyRelativePosition.y;
        }

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }
}
