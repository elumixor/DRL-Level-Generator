using System;
using NaughtyAttributes;
using UnityEngine;

namespace DRL.Behaviours {
    public class Trainer<TAction, TObservation> : MonoBehaviour {
        [SerializeField] Environment<TAction, TObservation> environment;
        [SerializeField] Agent<TAction, TObservation> agent;

        DRL.Trainer<TAction, TObservation> trainer;

        [SerializeField, MinValue(1)] int epochs;
        [SerializeField, MinValue(1)] int episodesPerEpoch;
        [SerializeField, MinValue(1)] int maximumEpisodeLength;

        void Start() {
            trainer = new DRL.Trainer<TAction, TObservation>(environment, agent, epochs, episodesPerEpoch, maximumEpisodeLength);
            trainer.StartTraining();
        }
    }
}