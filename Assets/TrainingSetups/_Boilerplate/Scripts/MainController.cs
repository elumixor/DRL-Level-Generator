using System.Collections.Generic;
using RLBehaviours;
using TrainingSetups._Boilerplate.Scripts.RL;
using UnityEngine;

namespace TrainingSetups._Boilerplate.Scripts
{
    public class MainController : MainController<State, Action, TrainingInstance, Agent, TrainingInstance>
    {
        /// <inheritdoc/>
        protected override void Train(List<List<(State state, Action action, float reward, State nextState)>> epoch)
        {
            Debug.Log("Training... sort of");
        }
    }
}
