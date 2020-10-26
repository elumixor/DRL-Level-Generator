using System;
using DRL.Behaviours;

namespace TrainingSetups._Boilerplate.Scripts.DRL {
    public class Environment : Environment<Action, State> {
        public override State ResetEnvironment() { throw new NotImplementedException(); }
        public override (State newState, float reward, bool isDone) Step(Action action) => throw new NotImplementedException();
    }
}