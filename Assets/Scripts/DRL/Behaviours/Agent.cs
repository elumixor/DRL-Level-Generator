﻿using UnityEngine;

namespace DRL.Behaviours {
    public abstract class Agent<TAction, TObservation> : MonoBehaviour, IAgent<TAction, TObservation> {
        public virtual void Initialize(IEnvironment<TAction, TObservation> environment) {}
        public virtual void OnEpisodeStarted() {}
        public abstract TAction GetAction(TObservation observation);
        public virtual void SaveStep(TObservation previousObservation, TAction action, float reward) {}
        public virtual void OnEpisodeFinished() {}
        public virtual void UpdateAgent() {}
    }
}