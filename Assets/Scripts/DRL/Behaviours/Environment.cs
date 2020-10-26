using System;
using NaughtyAttributes;
using UnityEngine;

namespace DRL.Behaviours {
    public abstract class Environment<TAction, TState> : MonoBehaviour, IEnvironment<TAction, TState> {
        [SerializeField, MinValue(1)] int stepFrequency;
        int currentStep;

        protected abstract TState CurrentState { get; }

        protected virtual void FixedUpdate() {
            if (!IsActive) return;

            if (currentStep < stepFrequency) {
                currentStep++;
                return;
            }

            Stepped(CurrentState);

            currentStep = 0;
        }

        public abstract void ResetEnvironment();
        public abstract (float reward, bool isDone) Step(TAction action);
        public event Action<TState> Stepped = delegate { };

        /// <summary>
        ///     Is set to true when the training session first begins
        /// </summary>
        public bool IsActive { get; set; }
    }
}