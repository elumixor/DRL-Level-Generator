﻿using System;

namespace Common.Exceptions
{
    public class BaseException : Exception
    {
        public BaseException(string message = "Unhandled base application exception has occurred") : base(message) { }
    }
}
