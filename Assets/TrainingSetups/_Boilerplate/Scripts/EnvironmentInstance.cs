using System;
using RL.RLBehaviours;
using TrainingSetups._Boilerplate.Scripts.RL;
using Action = TrainingSetups._Boilerplate.Scripts.RL.Action;

namespace TrainingSetups._Boilerplate.Scripts
{
    public class EnvironmentInstance : EnvironmentInstance<State, Action, Agent>
    {
        /// <inheritdoc/>
        public override State ResetEnvironment() => throw new NotImplementedException();

        /// <inheritdoc/>
        public override (State newState, float reward, bool isDone) Step(Action action) => throw new NotImplementedException();
    }
}
