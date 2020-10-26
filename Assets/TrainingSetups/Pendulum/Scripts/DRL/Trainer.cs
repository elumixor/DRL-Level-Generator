using DRL.Behaviours;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class Trainer : Trainer<Action, State, Environment, Agent> {
        [SerializeField, Range(0, 15)] float timeSpeed;

        void OnValidate() {
            Time.timeScale = timeSpeed;
            Time.fixedDeltaTime = 0.02f * timeSpeed;
        }
    }
}