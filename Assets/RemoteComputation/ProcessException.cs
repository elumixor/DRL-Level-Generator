using RL.Exceptions;

namespace RemoteComputation
{
    public class ProcessException : BaseException
    {
        public ProcessException(string message = "Unhandled process-related exception has occurred") : base(message) { }
    }
}
