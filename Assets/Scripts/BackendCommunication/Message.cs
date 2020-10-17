using System;
using System.Collections.Generic;
using System.Linq;
using Common.ByteConversions;

namespace BackendCommunication {
    public class Message : IByteConvertible {
        readonly IEnumerable<byte> data;
        readonly MessageHeader header;

        public Message(MessageHeader header, IEnumerable<byte> data) {
            this.header = header;
            this.data = data;
        }

        public IEnumerable<byte> ToBytes() {
            var data = this.data.ToArray();
            var result = new byte[data.Length + 1];
            result[0] = (byte) (header == MessageHeader.Inference ? 'i' : 't');

            Buffer.BlockCopy(data, 0, result, 1, data.Length);
            return result;
        }
    }
}