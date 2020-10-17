namespace DRL {
    public class Transition<TAction, TState> {
        public readonly TAction action;
        public readonly TState nextState;
        public readonly TState previousState;
        public readonly float reward;

        public Transition(TState previousState, TAction action, float reward, TState nextState) {
            this.previousState = previousState;
            this.action = action;
            this.reward = reward;
            this.nextState = nextState;
        }
    }
}