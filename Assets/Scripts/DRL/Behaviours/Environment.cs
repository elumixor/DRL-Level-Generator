using System;
using NaughtyAttributes;
using UnityEngine;

namespace DRL.Behaviours {
    public abstract class Environment<TAction, TObservation> : MonoBehaviour, IEnvironment<TAction, TObservation> {
        [SerializeField, MinValue(1)] int stepFrequency;

        int currentStep;
        public abstract void ResetEnvironment();
        public abstract (float reward, bool isDone) Step(TAction action);

        public event Action<TObservation> Stepped = delegate { };
        public bool IsActive { get; set; }

        protected virtual void Update() {
            if (!IsActive) return;

            if (currentStep < stepFrequency) {
                currentStep++;
                return;
            }

            Stepped(CurrentObservation);

            currentStep = 0;
        }

        protected abstract TObservation CurrentObservation { get; }
    }
}