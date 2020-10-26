using UnityEngine;

namespace RL.Behaviours {
    public abstract class Environment<TAction, TState> : MonoBehaviour, IEnvironment<TAction, TState> {
        public abstract TState ResetEnvironment();
        public abstract (TState newState, float reward, bool isDone) Step(TAction action);
    }
}