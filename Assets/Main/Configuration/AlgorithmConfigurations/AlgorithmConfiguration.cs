using System;
using System.Collections.Generic;
using Configuration.NN;

namespace Configuration.AlgorithmConfigurations
{
    [Serializable]
    public abstract class AlgorithmConfiguration
    {
        public abstract IEnumerable<ModuleConfiguration> ActorLayout(int stateSize, int actionSize);
        public abstract IEnumerable<byte> ToBytes(int stateSize, int actionSize);
    }
}
