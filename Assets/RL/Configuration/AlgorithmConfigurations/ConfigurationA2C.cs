using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;
using RL.Configuration.Dynamic;
using RL.Configuration.NN;
using RL.NN;
using RL.Serialization;
using Module = RL.NN.Module;

namespace RL.Configuration.AlgorithmConfigurations
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

        public override Module ConstructActorNN(int stateSize, int actionSize) =>
                networksType == A2CNetworksType.Separate
                        ? new Sequential(actor.Modules(stateSize, actionSize).Select(m => m.ToModule()))
                        : new Sequential(new Sequential(@base.Modules(stateSize, NNModuleDefinitions.INFER).Select(m => m.ToModule())),
                                         new Sequential(actorHead.Modules(NNModuleDefinitions.INFER, actionSize).Select(m => m.ToModule())));

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
