using System.Collections.Generic;
using Common;
using Common.ByteConversions;

namespace RemoteComputation
{
    public class Message
    {
        public IEnumerable<byte> Bytes { get; }

        Message(MessageType messageType, params IEnumerable<byte>[] data) =>
                Bytes = ((int) messageType).ToBytes().ConcatMany(data);

        enum MessageType
        {
            ObtainModel,
            RunTask,
        }

        public static Message ObtainModel() => new Message(MessageType.ObtainModel);

        public static Message RunTask(int id, RemoteTask task, IEnumerable<byte> argument) =>
                new Message(MessageType.RunTask, id.ToBytes(), ((int) task).ToBytes(), argument);
    }
}
