using System;
using System.Collections.Generic;
using Common.ByteConversions;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public struct Action : IByteSerializable {
        public bool tap;

        public void AssignFromBytes(byte[] bytes) { tap = bytes.ToFloat() > 0; }


        public IEnumerable<byte> ToBytes() { return (tap ? 1f : 0f).ToBytes(); }

        public int Size { get; }
        public float[] ArrayData { get; set; }
        public void FromBytes(IEnumerable<byte> bytes) { throw new NotImplementedException(); }
    }
}