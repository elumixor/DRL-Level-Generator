using System.Collections.Generic;
using System.Linq;
using Common.ByteConversions;
using DRL;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class Episode : IEpisode<InferenceTransition>, IByteConvertible {
        readonly List<InferenceTransition> transitions = new List<InferenceTransition>();

        public IEnumerable<byte> ToBytes() { return transitions.ToBytes(transitions.Count); }

        public void Add(InferenceTransition transition) { transitions.Add(transition); }

        public float TotalReward => transitions.Select(t => t.reward).Sum();
        public int Length => transitions.Count;
    }
}