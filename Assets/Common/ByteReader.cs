using System;
using System.Text;

namespace Common
{
    public class ByteReader
    {
        readonly byte[] bytes;
        int currentOffset;

        public ByteReader(byte[] bytes, int startOffset = 0)
        {
            this.bytes    = bytes;
            currentOffset = startOffset;
        }

        public int ReadInt()
        {
            var result = BitConverter.ToInt32(bytes, currentOffset);
            currentOffset += sizeof(int);
            return result;
        }

        public float ReadFloat()
        {
            var result = BitConverter.ToSingle(bytes, currentOffset);
            currentOffset += sizeof(float);
            return result;
        }

        public string ReadString()
        {
            var length = ReadInt();
            var result = Encoding.UTF8.GetString(bytes, currentOffset, length);
            currentOffset += length;
            return result;
        }
    }
}
