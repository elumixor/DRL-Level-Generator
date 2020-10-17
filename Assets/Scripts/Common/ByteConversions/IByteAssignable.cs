using System.Collections.Generic;

namespace Common.ByteConversions {
    public interface IByteAssignable {
        void FromBytes(IEnumerable<byte> bytes);
    }
}