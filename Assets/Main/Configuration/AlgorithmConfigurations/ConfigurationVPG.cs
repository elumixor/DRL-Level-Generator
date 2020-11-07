using System;
using System.Collections.Generic;
using Configuration.NN;

namespace Configuration.AlgorithmConfigurations
{
    [Serializable]
    public class ConfigurationVPG : AlgorithmConfiguration
    {
        public Layout actor = new Layout();
        public override IEnumerable<ModuleConfiguration> ActorLayout(int stateSize, int actionSize) => actor.Modules(stateSize, actionSize);

        public override IEnumerable<byte> ToBytes(int stateSize, int actionSize) => actor.ToBytes(stateSize, actionSize);
    }
}
