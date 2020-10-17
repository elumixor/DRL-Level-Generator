using System.Linq;
using Common.ByteConversions;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class State : IByteConvertible {
        readonly Vector2[] enemyPositions;
        readonly float playerPosition;
        readonly float angle;
        readonly float angularSpeed;
        readonly float upwardSpeed;

        public State(Vector2[] enemyPositions, float playerPosition, float angle, float angularSpeed, float upwardSpeed) {
            this.enemyPositions = enemyPositions;
            this.playerPosition = playerPosition;
            this.angle = angle;
            this.angularSpeed = angularSpeed;
            this.upwardSpeed = upwardSpeed;
        }

        public byte[] ToBytes() {
            var enemyPositionsBytes = enemyPositions.Select(p => p.ToBytes()).ToBytes();
            var result = ByteConverter.ConcatBytes(enemyPositionsBytes, playerPosition.ToBytes(), angle.ToBytes(), angularSpeed.ToBytes(),
                upwardSpeed.ToBytes());
            return result;
        }
    }
}