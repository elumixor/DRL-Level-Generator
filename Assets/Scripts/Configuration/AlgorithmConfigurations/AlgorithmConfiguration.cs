using System;
using Configuration.NN;
using UnityEngine;

namespace Configuration.AlgorithmConfigurations {
    [Serializable]
    public abstract class AlgorithmConfiguration {
        public abstract Layout ActorLayout { get; }
    }
}