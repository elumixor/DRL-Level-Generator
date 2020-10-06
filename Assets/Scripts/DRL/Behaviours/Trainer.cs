using System;
using NaughtyAttributes;
using UnityEngine;

namespace DRL.Behaviours {
    public class Trainer<TAction, TState> : MonoBehaviour {
        [SerializeField] Environment<TAction, TState> environment;
        [SerializeField] Agent<TAction, TState> agent;
        [SerializeField, Range(0, 15)] float timeSpeed;

        DRL.Trainer<TAction, TState> trainer;

        [SerializeField, MinValue(1)] int epochs;
        [SerializeField, MinValue(1)] int episodesPerEpoch;
        [SerializeField, MinValue(1)] int maximumEpisodeLength;

        void Start() {
            trainer = new DRL.Trainer<TAction, TState>(environment, agent, epochs, episodesPerEpoch, maximumEpisodeLength);
            trainer.StartTraining();
        }

        void OnValidate() {
            Time.timeScale = timeSpeed;
            // Time.fixedDeltaTime = 0.02f * (1 - timeSpeed);
        }
    }
}