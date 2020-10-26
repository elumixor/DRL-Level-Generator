using UnityEngine;

namespace RL.Behaviours {
    public abstract class Agent<TAction, TState> : MonoBehaviour, IAgent<TAction, TState> {
        public abstract TAction GetAction(TState observation);
        public virtual void OnEnvironmentCreated(IEnvironment<TAction, TState> environment) { }
        public virtual void OnTransition(TState previousState, TAction action, float reward, TState nextState) { }
        public virtual void OnEpisodeStarted() { }
        public virtual void OnEpisodeFinished() { }
        public virtual void OnEpochFinished() { }
    }
}