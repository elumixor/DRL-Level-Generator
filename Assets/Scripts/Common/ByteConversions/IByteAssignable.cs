namespace Common.ByteConversions {
    public interface IByteAssignable {
        /// <summary>
        ///     Assigns self from bytes and returns the number of bytes read
        /// </summary>
        int AssignFromBytes(byte[] bytes, int start = 0);
    }
}