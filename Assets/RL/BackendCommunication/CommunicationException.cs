using RL.Exceptions;

namespace RL.BackendCommunication
{
    public class CommunicationException : BaseException
    {
        public CommunicationException(string message = "Unhandled communication exception has occurred") : base(message) { }
    }
}
