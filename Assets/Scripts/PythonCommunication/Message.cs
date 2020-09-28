using System;
using Common;

namespace PythonCommunication {
    public class Message : IByteConvertible {
        readonly MessageHeader header;
        readonly byte[] data;

        public Message(MessageHeader header, byte[] data) {
            this.header = header;
            this.data = data;
        }

        public byte[] ToBytes() {
            var result = new byte[data.Length + 1];
            result[0] = (byte) (header == MessageHeader.Inference ? 'i' : 't');
            
            Buffer.BlockCopy(data, 0, result, 1, data.Length);
            return result;
        }
    }
}