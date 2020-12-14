using System.Collections.Generic;
using Common;
using Common.ByteConversions;

namespace RemoteComputation
{
    public class Message
    {
        public IEnumerable<byte> Bytes { get; }

        Message(MessageType messageType, params IEnumerable<byte>[] data) => Bytes = ((int) messageType).ToBytes().ConcatMany(data);

        enum MessageType
        {
            ObtainModel,
            LoadModel,
            SaveModel,
            RunTask,
        }

        public static Message ObtainModel() => new Message(MessageType.ObtainModel);

        public static Message ObtainModel(IEnumerable<byte> args) => new Message(MessageType.ObtainModel, args);

        public static Message LoadModel(string path) => new Message(MessageType.LoadModel, path.ToBytes());

        public static Message SaveModel(int modelId, string path) => new Message(MessageType.SaveModel, modelId.ToBytes(), path.ToBytes());

        public static Message RunTask(int id, RemoteTask task, IEnumerable<byte> argument) =>
                new Message(MessageType.RunTask, id.ToBytes(), ((int) task).ToBytes(), argument);
    }
}
