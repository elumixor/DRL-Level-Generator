using Common.ByteConversions;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public struct Action {
        public bool tap;

        public void AssignFromBytes(byte[] bytes) { tap = bytes.ToFloat() > 0; }

        public byte[] ToBytes() => (tap ? 1f : 0f).ToBytes();

        public int Size { get; }
        public float[] ArrayData { get; set; }
    }
}