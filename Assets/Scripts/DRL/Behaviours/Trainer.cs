using NaughtyAttributes;
using UnityEngine;

namespace DRL.Behaviours {
    public class Trainer<TAction, TState> : MonoBehaviour {
        [SerializeField] Agent<TAction, TState> agent;
        [SerializeField] Environment<TAction, TState> environment;
        [SerializeField, MinValue(1)] int episodesPerEpoch;

        [SerializeField, MinValue(1)] int epochs;
        [SerializeField, MinValue(1)] int maximumEpisodeLength;
        [SerializeField, Range(0, 15)] float timeSpeed;

        DRL.Trainer<TAction, TState> trainer;

        public void StartTraining() {
            trainer = new DRL.Trainer<TAction, TState>(environment, agent, epochs, episodesPerEpoch, maximumEpisodeLength);
            trainer.StartTraining();
        }

        void OnValidate() {
            Time.timeScale = timeSpeed;
            // Time.fixedDeltaTime = 0.02f * (1 - timeSpeed);
        }
    }
}