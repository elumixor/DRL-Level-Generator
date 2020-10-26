using System;
using RL.Behaviours;

namespace TrainingSetups._Boilerplate.Scripts.RL {
    public class Agent : Agent<Action, State> {
        public override Action GetAction(State observation) => throw new NotImplementedException();
    }
}