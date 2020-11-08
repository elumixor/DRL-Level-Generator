using System;
using System.Collections.Generic;
using System.Linq;
using Configuration.NN;
using NN;
using Serialization;

namespace Configuration.AlgorithmConfigurations
{
    [Serializable]
    public class ConfigurationVPG : AlgorithmConfiguration
    {
        public Layout actor = new Layout();

        public override Module ConstructActorNN(int stateSize, int actionSize) =>
                new Sequential(actor.Modules(stateSize, actionSize).Select(m => m.ToModule()));

        public override IEnumerable<byte> ToBytes(int stateSize, int actionSize) => actor.ToBytes(stateSize, actionSize);
    }
}
