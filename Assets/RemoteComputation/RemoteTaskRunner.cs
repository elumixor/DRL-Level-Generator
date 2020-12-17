using System.Collections.Generic;
using System.Threading.Tasks;
using Common;

namespace RemoteComputation
{
    public static class RemoteTaskRunner
    {
        /// <summary> Performs a remote task (computation) on a remote backend </summary>
        /// <param name="modelId"> Model Id that will be used on backend </param>
        /// <param name="task"> Task to be performed </param>
        /// <param name="arguments"> Argument(s) as bytes </param>
        /// <param name="onComputed"> Callback to be executed once the task is completed </param>
        public static async Task<ByteReader> RunTask(int modelId, RemoteTask task, IEnumerable<byte> arguments) =>
                await Communicator.Send(Message.RunTask(modelId, task, arguments));
    }
}
