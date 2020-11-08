using System;
using System.Collections.Generic;
using NN;

namespace Configuration.AlgorithmConfigurations
{
    [Serializable]
    public abstract class AlgorithmConfiguration
    {
        public abstract Module ConstructActorNN(int stateSize, int actionSize);
        public abstract IEnumerable<byte> ToBytes(int stateSize, int actionSize);
    }
}
