using System;
using RL.NN;
using RL.RL;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts
{
    public class Agent : MonoBehaviour, IAgent<State, int>, INNAgent
    {
        /// <inheritdoc/>
        public int GetAction(State state) => throw new NotImplementedException();

        /// <inheritdoc/>
        public void InitializeNN(Module nn) { throw new NotImplementedException(); }

        /// <inheritdoc/>
        public void SetParameters(StateDict stateDict) { throw new NotImplementedException(); }
    }
}
