using System;
using DRL.Behaviours;

namespace TrainingSetups.Boilerplate.Scripts.DRL {
    public class Agent : Agent<Action, State> {
        public override Action GetAction(State observation) => throw new NotImplementedException();
    }
}