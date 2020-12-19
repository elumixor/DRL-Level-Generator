using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using RemoteComputation.Logging;
using RemoteComputation.Models;

namespace RemoteComputation
{
    public class Message
    {
        public IEnumerable<byte> Bytes { get; }

        Message(MessageType messageType, params IEnumerable<byte>[] data) => Bytes = ((int) messageType).ToBytes().ConcatMany(data);

        enum MessageType
        {
            ObtainModel = 0,
            LoadModel = 1,
            SaveModel = 2,
            RunTask = 3,
            SetLogOptions = 4,

            Test = 99,
        }

        public static Message ObtainModel(ModelType modelType) => new Message(MessageType.ObtainModel, ((int) modelType).ToBytes());

        public static Message ObtainModel(ModelType modelType, params IEnumerable<byte>[] args) =>
                new Message(MessageType.ObtainModel, ((int) modelType).ToBytes().ConcatMany(args));

        public static Message LoadModel(string path) => new Message(MessageType.LoadModel, path.ToBytes());

        public static Message SaveModel(int modelId, string path) => new Message(MessageType.SaveModel, modelId.ToBytes(), path.ToBytes());

        public static Message RunTask(int id, RemoteTask task, IEnumerable<byte> argument) =>
                new Message(MessageType.RunTask, id.ToBytes(), ((int) task).ToBytes(), argument);

        public static Message Test(params IEnumerable<byte>[] args) => new Message(MessageType.Test, args);

        public static Message SetLogOptions(int modelId, LogOptions logOptions) =>
                new Message(MessageType.SetLogOptions, modelId.ToBytes(), logOptions.Bytes);
    }
}
