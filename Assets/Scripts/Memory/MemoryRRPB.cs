﻿using System.Collections.Generic;
using Common.ByteConversions;
using DRL;
using UnityEngine;
using Random = System.Random;

namespace Memory {
    /// <summary>
    ///     Memory that [R]eplaces the [R]andom episode but [P]reserves the [B]est episode (in terms of achieved reward)
    /// </summary>
    public class MemoryRRPB<TEpisode, TTransition> : IMemory<TEpisode, TTransition> where TTransition : IByteConvertible
        where TEpisode : IEpisode<TTransition>, IByteConvertible {
        static readonly Random generator = new Random();
        readonly List<TEpisode> episodes;
        readonly int totalSize;

        (int index, float value) currentBest = (-1, float.NegativeInfinity);

        public MemoryRRPB(int totalSize) {
            this.totalSize = totalSize;
            episodes = new List<TEpisode>(totalSize);
        }

        public IEnumerable<byte> ToBytes() { return episodes.ToBytes(episodes.Count); }

        public void Push(TEpisode episode) {
            var isBetter = episode.TotalReward > currentBest.value;

            if (!IsFull) {
                episodes.Add(episode);

                if (isBetter) currentBest = (episodes.Count - 1, episode.TotalReward);

                return;
            }

            var index = generator.Next(totalSize);

            Debug.Log($"Total: {totalSize}. Current {episodes.Count}. Generated: {index}");

            if (isBetter) {
                currentBest = (index, episode.TotalReward);
            } else if (index == currentBest.index) {
                index = (index + 1) % totalSize;
                Debug.Log($"Modifying to {index}");
            }

            episodes[index] = episode;
        }

        public bool IsFull => episodes.Count == totalSize;
    }
}