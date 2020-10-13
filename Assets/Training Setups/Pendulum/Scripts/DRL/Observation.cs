using System.Linq;
using Common.ByteConversions;
using UnityEngine;

namespace Training_Setups.Pendulum.Scripts.DRL {
    public class Observation : IByteConvertible {
        public Vector2[] enemiesPositions;
        public float playerPosition;
        public byte[] ToBytes() => enemiesPositions.Select(e => e.ToBytes()).ToBytes();
    }
}