using System.Linq;
using Common;
using UnityEngine;

namespace Implementation.PythonInference {
    public class State : IByteConvertible {
        readonly Vector2[] enemyPositions;
        readonly float playerPosition;
        readonly float angle;
        readonly float anglularSpeed;
        readonly float upwardSpeed;

        public State(Vector2[] enemyPositions, float playerPosition, float angle, float anglularSpeed, float upwardSpeed) {
            this.enemyPositions = enemyPositions;
            this.playerPosition = playerPosition;
            this.angle = angle;
            this.anglularSpeed = anglularSpeed;
            this.upwardSpeed = upwardSpeed;
        }

        public byte[] ToBytes() {
            var enemyPositionsBytes = enemyPositions.Select(p => p.ToBytes()).ToBytes();
            var result = ByteConverter.ConcatBytes(enemyPositionsBytes, playerPosition.ToBytes(), angle.ToBytes(), anglularSpeed.ToBytes(),
                upwardSpeed.ToBytes());
            return result;
        }
    }
}