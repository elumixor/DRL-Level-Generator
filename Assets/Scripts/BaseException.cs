using System;

public class BaseException : Exception {
    protected BaseException(string message = "Unhandled base application exception has occurred") : base(message) { }
}