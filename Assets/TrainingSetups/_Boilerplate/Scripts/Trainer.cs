using System;
using System.Collections.Generic;
using RL.RLBehaviours;
using TrainingSetups._Boilerplate.Scripts.RL;
using Action = TrainingSetups._Boilerplate.Scripts.RL.Action;

namespace TrainingSetups._Boilerplate.Scripts
{
    public class Trainer : Trainer<State, Action, EnvironmentInstance, Agent, EnvironmentInstance>
    {
        /// <inheritdoc/>
        protected override IEnumerable<byte> TransitionToBytes((State state, Action action, float reward, State nextState) transition) =>
                throw new NotImplementedException();
    }
}
