using System.Collections;
using System.Collections.Generic;
using Serialization;

namespace TrainingSetups.LeftRight.Scripts
{
    public readonly struct State : IEnumerable<float>
    {
        [Structural] readonly float x;

        public State(float x) => this.x = x;

        public IEnumerator<float> GetEnumerator() { yield return x; }
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }
}
