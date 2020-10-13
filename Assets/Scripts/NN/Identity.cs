namespace NN {
    public class Identity : Module {
        public override float[] Forward(float[] input) => input;
    }
}