using System.Collections.Generic;
using RLBehaviours;
using TrainingSetups._Boilerplate.Scripts.RL;
using UnityEngine;

namespace TrainingSetups._Boilerplate.Scripts
{
    public class Trainer : Trainer<State, Action, EnvironmentInstance, Agent, EnvironmentInstance>
    {
        /// <inheritdoc/>
        protected override void Train(List<List<(State state, Action action, float reward, State nextState)>> epoch) { Debug.Log("Training... sort of"); }
    }
}
