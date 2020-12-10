using System;
using System.Threading.Tasks;

namespace RemoteComputation {
    // Abstracts the computation
    // 
    public class RemoteModel {
        // uses this to communicate with the backend
        public readonly int id;
        public event Action BecameAvailable = delegate { };

        // Statically will manage stuff

        // Each model might be
        //   1. Initialized (with NNConfiguration parameters)
        //   2. Perform various requests
        //        Each request will have a task header and arguments as byte array 
        // Examples of requests:
        // 1. Train
        // 2. Infer
        // 3. Evaluate difficulty

        /// <summary>
        /// Creates a new model and initializes stuff on backend 
        /// </summary>
        /// <returns></returns>
        public static RemoteModel Obtain() {
            // what about Futures?
            // should not block, instead fires an event
            throw new NotImplementedException();
        }

        public async Task<byte[]> Compute(RemoteTask task, byte[] argument) {
            // should not block
            throw new NotImplementedException();
        }
    }
}