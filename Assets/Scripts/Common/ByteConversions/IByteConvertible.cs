using System.Collections.Generic;
using JetBrains.Annotations;

namespace Common.ByteConversions {
    public interface IByteConvertible {
        [Pure]
        IEnumerable<byte> ToBytes();
    }
}