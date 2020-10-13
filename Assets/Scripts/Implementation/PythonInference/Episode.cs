using System.Collections.Generic;
using System.Linq;
using Common;
using DRL;

namespace Implementation.PythonInference {
    public class Episode : IEpisode<InferenceTransition> {
        readonly List<InferenceTransition> transitions = new List<InferenceTransition>();
        public void Add(InferenceTransition transition) => transitions.Add(transition);
        public float TotalReward => transitions.Select(t => t.reward).Sum();
        public int Length => transitions.Count;

        public byte[] ToBytes() => transitions.ToBytes(true);
    }
}