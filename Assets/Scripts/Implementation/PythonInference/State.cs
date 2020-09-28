namespace Implementation.PythonInference {
    public class State : IByteConvertible {
        // state contains:
        // - positions of the enemies (2) * 3 = (6)
        // - position of the player (handle) (1)
        // - current angle (1)
        // - current angular speed (1)
        // - current upward speed (1)
        // total: 6 + 1 + 1 + 1 + 1 = 10
        readonly Vector2[] enemyPositions;
        private Vector2 playerPosition;
        private float angle;
        private float anglularSpeed;
        private float upwardSpeed;

        public State(Vector2[] enemyPositions, Vector2 playerPosition,
            float angle, float anglularSpeed, float upwardSpeed) {
            this.enemyPositions = enemyPositions;
            this.playerPosition = playerPosition;
            this.angle = angle;
            this.anglularSpeed = anglularSpeed;
            this.upwardSpeed = upwardSpeed;
        }

        public byte[] ToBytes() {
            return ByteConverter.ConcatBytes(
                enemyPositions.Select(p => p.ToBytes()).ToArray(), 
                playerPosition.ToBytes(), 
                angle.ToBytes(),
                anglularSpeed.ToBytes(),
                upwardSpeed.ToBytes(),
                angle.ToBytes())
        }
    }
}