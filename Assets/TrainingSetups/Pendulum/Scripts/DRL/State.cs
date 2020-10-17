using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class State : IByteConvertible {
        readonly float angle;
        readonly float angularSpeed;
        readonly Vector2[] enemyPositions;
        readonly float playerPosition;
        readonly float upwardSpeed;

        public State(Vector2[] enemyPositions, float playerPosition, float angle, float angularSpeed, float upwardSpeed) {
            this.enemyPositions = enemyPositions;
            this.playerPosition = playerPosition;
            this.angle = angle;
            this.angularSpeed = angularSpeed;
            this.upwardSpeed = upwardSpeed;
        }

        public IEnumerable<byte> ToBytes() {
            var enemyPositionsBytes = enemyPositions.ToBytes(enemyPositions.Length);

            var result = enemyPositionsBytes.ConcatMany(playerPosition.ToBytes(), angle.ToBytes(), angularSpeed.ToBytes(),
                upwardSpeed.ToBytes());
            return result;
        }
    }
}