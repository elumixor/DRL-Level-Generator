using System;
using System.Collections.Generic;
using Common;

namespace RemoteComputation
{
    // Abstracts the various tasks computation, that should be done on backend
    //
    public class RemoteModel
    {
        // uses this to communicate with the backend
        readonly int id;
        RemoteModel(int id) => this.id = id;

        /// <summary> Creates a new model and initializes stuff on backend </summary>
        public static void Obtain(Action<RemoteModel> onObtained) =>
                Communicator.Send(Message.ObtainModel(),
                                  reader => {
                                      var modelId = reader.ReadInt();
                                      var model = new RemoteModel(modelId);
                                      onObtained(model);
                                  });

        /// <summary> Performs a remote task (computation) on a remote backend </summary>
        /// <param name="task"> Task to be performed </param>
        /// <param name="argument"> Argument(s) as bytes </param>
        /// <param name="onComputed"> Callback to be executed once the task is completed </param>
        public void RunTask(RemoteTask task, IEnumerable<byte> argument, Action<ByteReader> onComputed)
        {
            Communicator.Send(Message.RunTask(id, task, argument), onComputed);
        }
    }
}
