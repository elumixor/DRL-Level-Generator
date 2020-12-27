using System.Collections.Generic;
using System.Linq;
using Common.ByteConversions;

namespace RemoteComputation.Logging
{
    public class LogOptions : Dictionary<LogOptionName, LogOption>, IByteConvertible
    {
        /// <inheritdoc/>
        public LogOptions(params (LogOptionName optionName, LogOption optionValue)[] options)
        {
            foreach (var (optionName, optionValue) in options) this[optionName] = optionValue;
        }

        /// <inheritdoc/>
        public IEnumerable<byte> Bytes => Count.ToBytes().Concat(this.SelectMany(kvp => ((int) kvp.Key).ToBytes().Concat(kvp.Value.Bytes)));
    }
}
