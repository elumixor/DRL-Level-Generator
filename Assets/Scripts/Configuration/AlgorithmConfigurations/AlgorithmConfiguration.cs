using System;
using Configuration.NN;

namespace Configuration.AlgorithmConfigurations {
    [Serializable]
    public abstract class AlgorithmConfiguration {
        public abstract Layout ActorLayout { get; }
    }
}