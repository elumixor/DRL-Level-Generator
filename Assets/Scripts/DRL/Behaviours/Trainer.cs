using NaughtyAttributes;
using UnityEngine;

namespace DRL.Behaviours {
    public class Trainer<TAction, TState, TEnvironment, TAgent> : MonoBehaviour
        where TEnvironment : Environment<TAction, TState> where TAgent : Agent<TAction, TState> {
        [SerializeField] protected TAgent agent;
        [SerializeField] protected TEnvironment environment;
        [SerializeField, MinValue(1)] int episodesPerEpoch;
        [SerializeField, MinValue(1)] int epochs;
        [SerializeField, MinValue(1)] int maximumEpisodeLength;

        Trainer<TAction, TState> trainer;

        public void StartTraining() {
            trainer = new Trainer<TAction, TState>(environment, agent, epochs, episodesPerEpoch, maximumEpisodeLength);
            trainer.StartTraining();
        }
    }
}