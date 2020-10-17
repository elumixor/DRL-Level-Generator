using System.Collections.Generic;
using Common.ByteConversions;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public struct Action : IByteSerializable {
        public bool tap;
        public IEnumerable<byte> ToBytes() { return (tap ? 1f : -1f).ToBytes(); }

        public int AssignFromBytes(byte[] bytes, int start = 0) {
            var value = bytes.ToFloat(start);
            tap = value > 0;
            return sizeof(float);
        }
    }
}