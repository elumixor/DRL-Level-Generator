using System;
using System.Collections.Generic;
using Common.ByteConversions;
using Configuration.NN;

namespace Configuration.AlgorithmConfigurations
{
    [Serializable]
    public abstract class AlgorithmConfiguration : IByteConvertible
    {
        public abstract Layout ActorLayout { get; }
        public abstract IEnumerable<byte> ToBytes();
    }
}
