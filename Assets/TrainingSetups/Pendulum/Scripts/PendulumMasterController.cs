using TrainingSetups.Pendulum.Scripts.RL;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts {
    public class PendulumMainController : MainController<Action, State, Environment, Agent> {
        [SerializeField, Range(0, 15)] float timeSpeed;

        void OnValidate() {
            Time.timeScale = timeSpeed;
            Time.fixedDeltaTime = 0.02f * timeSpeed;
        }
    }
}