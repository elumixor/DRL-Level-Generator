using System;
using System.Threading.Tasks;
using UnityEngine;

namespace Common
{
    public class WaitForTask : CustomYieldInstruction
    {
        readonly float timeout;
        readonly Task task;
        float elapsed;

        /// <inheritdoc/>
        public WaitForTask(Action task, float timeout = float.PositiveInfinity)
        {
            this.timeout = timeout;
            this.task    = Task.Run(task);
        }

        public WaitForTask(Func<Task> task, float timeout = float.PositiveInfinity)
        {
            this.timeout = timeout;
            this.task    = Task.Run(task);
        }

        public WaitForTask(Task task, float timeout = float.PositiveInfinity)
        {
            this.task    = task;
            this.timeout = timeout;
        }

        /// <inheritdoc/>
        public override bool keepWaiting {
            get {
                elapsed += Time.deltaTime;

                if (task.IsFaulted) {
                    Debug.LogException(task.Exception);
                    return false;
                }

                if (Input.GetKeyDown(KeyCode.Escape)) {
                    Debug.LogError("Task interrupted");
                    return false;
                }

                var taskDone = task.IsCompleted || task.IsCanceled;
                return !taskDone && elapsed < timeout;
            }
        }
    }
}
