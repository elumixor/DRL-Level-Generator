using Common;
using Common.Exceptions;

namespace RemoteComputation
{
    public class CommunicationException : BaseException
    {
        public CommunicationException(string message = "Unhandled communication exception has occurred") : base(message) { }
    }
}
