using DRL.Behaviours;

namespace Implementation.Dummy {
    public class DummyAgent : Agent<DummyAction, DummyObservation> {
        // This silly agent will tap when it gets close to an enemy
        public override DummyAction GetAction(DummyObservation observation) {
            return new DummyAction {tap = observation.distanceToClosest < 1};
        }
    }
}