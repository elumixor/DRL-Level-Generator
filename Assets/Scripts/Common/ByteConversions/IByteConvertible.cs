using JetBrains.Annotations;

namespace Common.ByteConversions {
    public interface IByteConvertible {
        [Pure]
        byte[] ToBytes();
    }
}