using DRL;
using DRL.Behaviours;
using UnityEngine;

namespace Implementation {
    public class MyAgent : Agent<MyAction, MyObservation> {
        // This silly agent will tap when it gets close to an enemy
        public override MyAction GetAction(MyObservation observation) {
            return new MyAction {tap = observation.distanceToClosest < 1};
        }
    }
}