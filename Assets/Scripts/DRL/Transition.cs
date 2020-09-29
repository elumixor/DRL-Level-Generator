using Common;

namespace DRL {
    public class Transition<TAction, TState> {
        public readonly TState previousState;
        public readonly TAction action;
        public readonly float reward;
        public readonly TState nextState;

        public Transition(TState previousState, TAction action, float reward, TState nextState) {
            this.previousState = previousState;
            this.action = action;
            this.reward = reward;
            this.nextState = nextState;
        }
    }
}