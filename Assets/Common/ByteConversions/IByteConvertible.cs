using System.Collections.Generic;
using JetBrains.Annotations;

namespace Common.ByteConversions
{
    public interface IByteConvertible
    {
        /// Serializes an object to byte array
        IEnumerable<byte> Bytes { get; }
    }
}
