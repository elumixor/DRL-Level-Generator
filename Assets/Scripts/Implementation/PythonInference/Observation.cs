using System.Linq;
using Common;
using UnityEngine;

namespace Implementation.PythonInference {
    public class Observation : IByteConvertible {
        public Vector2[] enemiesPositions;
        public float playerPosition;
        public byte[] ToBytes() => enemiesPositions.Select(e => e.ToBytes()).ToBytes();
    }
}