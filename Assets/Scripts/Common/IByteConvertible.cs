using JetBrains.Annotations;

namespace Common {
    public interface IByteConvertible {
        [Pure]
        byte[] ToBytes();
    }
}