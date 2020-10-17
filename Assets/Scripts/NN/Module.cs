namespace NN {
    public abstract class Module {
        public abstract float[] Forward(float[] input);
        public virtual void LoadStateDict(StateDict stateDict) { }
    }
}