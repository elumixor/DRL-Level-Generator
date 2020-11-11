using System;
using System.Collections.Generic;
using RL.NN;

namespace RL.Configuration.AlgorithmConfigurations
{
    [Serializable]
    public abstract class AlgorithmConfiguration
    {
        public abstract Module ConstructActorNN(int stateSize, int actionSize);
        public abstract IEnumerable<byte> ToBytes(int stateSize, int actionSize);
    }
}
