using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;
using Configuration.Dynamic;
using Configuration.NN;

namespace Configuration.AlgorithmConfigurations
{
    [Serializable]
    public class ConfigurationA2C : AlgorithmConfiguration
    {
        public enum A2CNetworksType
        {
            TwoHeaded,
            Separate,
        }

        public Layout actor = new Layout();
        public Layout critic = new Layout();

        public Layout @base = new Layout();
        public Layout actorHead = new Layout();
        public Layout criticHead = new Layout();

        public A2CNetworksType networksType;

        public override IEnumerable<ModuleConfiguration> ActorLayout(int stateSize, int actionSize) =>
                networksType == A2CNetworksType.Separate
                        ? actor.Modules(stateSize, actionSize)
                        : @base.Modules(stateSize, NNModuleDefinitions.INFER).Concat(actorHead.Modules(NNModuleDefinitions.INFER, actionSize));

        public override IEnumerable<byte> ToBytes(int stateSize, int actionSize)
        {
            var networksBytes = networksType == A2CNetworksType.Separate
                                        ? actor.ToBytes(stateSize, actionSize).Concat(critic.ToBytes(stateSize, 1))
                                        : @base.ToBytes(stateSize, NNModuleDefinitions.INFER)
                                               .ConcatMany(actorHead.ToBytes(NNModuleDefinitions.INFER, actionSize),
                                                           criticHead.ToBytes(NNModuleDefinitions.INFER, 1));

            return networksType.ToString().ToBytes().Concat(networksBytes);
        }
    }
}
