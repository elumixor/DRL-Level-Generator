using System;
using NaughtyAttributes;
using UnityEngine;

namespace DRL.Behaviours {
    public abstract class Environment<TAction, TState> : MonoBehaviour, IEnvironment<TAction, TState> {
        int currentStep;
        [SerializeField, MinValue(1)] int stepFrequency;

        protected abstract TState CurrentState { get; }

        public abstract void ResetEnvironment();
        public abstract (float reward, bool isDone) Step(TAction action);
        public event Action<TState> Stepped = delegate { };
        public bool IsActive { get; set; }

        protected virtual void FixedUpdate() {
            if (!IsActive) return;

            if (currentStep < stepFrequency) {
                currentStep++;
                return;
            }

            Stepped(CurrentState);

            currentStep = 0;
        }
    }
}