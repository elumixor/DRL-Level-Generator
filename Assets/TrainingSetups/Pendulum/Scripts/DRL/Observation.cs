using System.Collections.Generic;
using Common.ByteConversions;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class Observation : IByteConvertible {
        public Vector2[] enemiesPositions;
        public float playerPosition;
        public IEnumerable<byte> ToBytes() { return enemiesPositions.ToBytes(enemiesPositions.Length); }
    }
}