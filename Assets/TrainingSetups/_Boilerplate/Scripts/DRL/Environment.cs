using System;
using DRL.Behaviours;

namespace TrainingSetups._Boilerplate.Scripts.DRL {
    public class Environment : Environment<Action, State> {
        protected override State CurrentState => throw new NotImplementedException();
        public override void ResetEnvironment() { throw new NotImplementedException(); }
        public override (float reward, bool isDone) Step(Action action) => throw new NotImplementedException();
    }
}