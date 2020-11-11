using System;
using RL.RL;
using UnityEngine;

namespace TrainingSetups._Boilerplate.Scripts.RL
{
    public class Agent : MonoBehaviour, IAgent<State, Action>
    {
        /// <inheritdoc/>
        public Action GetAction(State state) => throw new NotImplementedException();
    }
}
