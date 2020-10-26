using System;
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

        [SerializeField, MinValue(1)] int framesForStep;

        int currentFrame;
        
        public Trainer<TAction, TState> trainer { get; private set; }

        bool isTraining;
        
        public void StartTraining() {
            trainer = new Trainer<TAction, TState>(environment, agent, epochs, episodesPerEpoch, maximumEpisodeLength);
            isTraining = true;
            trainer.StartTraining();
            trainer.TrainingFinished += () => Debug.Log("Training finished!");
        }

        void Update() {
            if (!isTraining) return;

            if (currentFrame < framesForStep) {
                currentFrame++;
                return;
            }

            currentFrame = 0;            
            trainer.Step();
        }
    }
}