using System;
using RLBehaviours;
using TrainingSetups.Pendulum.Scripts.RL;
using Action = TrainingSetups.Pendulum.Scripts.RL.Action;

namespace TrainingSetups.Pendulum.Scripts
{
    public class EnvironmentInstance : EnvironmentInstance<State, Action, Agent>
    {
        /// <inheritdoc/>
        public override State ResetEnvironment() => throw new NotImplementedException();

        /// <inheritdoc/>
        public override (State newState, float reward, bool isDone) Step(Action action) => throw new NotImplementedException();
    }
}
