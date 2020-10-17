using System.Collections.Generic;
using Common.ByteConversions;
using DRL;
using UnityEngine;
using Random = System.Random;

namespace Memory {
    /// <summary>
    /// Memory that [R]eplaces the [R]andom episode but [P]reserves the [B]est episode (in terms of achieved reward)
    /// </summary>
    public class MemoryRRPB<TEpisode, TTransition> : IMemory<TEpisode, TTransition>
        where TTransition : IByteConvertible where TEpisode : IEpisode<TTransition> {
        readonly int totalSize;
        readonly List<TEpisode> episodes;

        (int index, float value) currentBest = (-1, float.NegativeInfinity);

        static readonly Random generator = new Random();

        public MemoryRRPB(int totalSize) {
            this.totalSize = totalSize;
            episodes = new List<TEpisode>(totalSize);
        }

        public byte[] ToBytes() => episodes.ToBytes(true);

        public void Push(TEpisode episode) {
            var isBetter = episode.TotalReward > currentBest.value;

            if (!IsFull) {
                episodes.Add(episode);

                if (isBetter) currentBest = (episodes.Count - 1, episode.TotalReward);

                return;
            }

            var index = generator.Next(totalSize);

            Debug.Log($"Total: {totalSize}. Current {episodes.Count}. Generated: {index}");

            if (isBetter) currentBest = (index, episode.TotalReward);
            else if (index == currentBest.index) {
                index = (index + 1) % totalSize;
                Debug.Log($"Modifying to {index}");
            }

            episodes[index] = episode;
        }

        public bool IsFull => episodes.Count == totalSize;
    }
}