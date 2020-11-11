using System.Collections.Generic;
using JetBrains.Annotations;

namespace RL.Common.ByteConversions
{
    public interface IByteConvertible
    {
        [Pure] IEnumerable<byte> ToBytes();
    }
}
