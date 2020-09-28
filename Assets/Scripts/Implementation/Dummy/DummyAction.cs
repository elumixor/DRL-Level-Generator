using Common;

namespace Implementation.Dummy {
    public struct DummyAction : IByteAssignable {
        public bool tap;

        public void AssignFromBytes(byte[] bytes) { tap = bytes.ToInt() > 0; }
    }
}