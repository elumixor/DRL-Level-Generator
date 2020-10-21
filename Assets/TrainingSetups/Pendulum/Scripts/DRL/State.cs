using System.Collections;
using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using Serialization;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class State : IEnumerable<float> {
        [Structural]
        readonly float angle;
        [Structural]
        readonly float angularSpeed;
        [Structural]
        readonly float playerPosition;
        [Structural]
        readonly float upwardSpeed;

        public State(float playerPosition, float angle, float angularSpeed, float upwardSpeed) {
            this.playerPosition = playerPosition;
            this.angle = angle;
            this.angularSpeed = angularSpeed;
            this.upwardSpeed = upwardSpeed;
        }

        public IEnumerator<float> GetEnumerator() {
            yield return angle;
            yield return angularSpeed;
            yield return playerPosition;
            yield return upwardSpeed;
        }

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }
}