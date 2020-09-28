using Common;

namespace Implementation.Dummy {
    public struct DummyAction : IByteConvertible, IByteAssignable {
        public bool tap;

        public void AssignFromBytes(byte[] bytes) { tap = bytes.ToInt() > 0; }
        public byte[] ToBytes() => (tap ? 1f : 0f).ToBytes();
    }
}