using Common;
using Common.ByteConversions;

namespace Implementation.Dummy {
    public struct DummyObservation : IByteConvertible {
        public float distanceToClosest;
        public byte[] ToBytes() => distanceToClosest.ToBytes();
    }
}