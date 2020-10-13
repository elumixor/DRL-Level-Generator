namespace NN {
    public class Sequential : Module {
        readonly Module[] layers;
        
        public Sequential(Module[] layers) => this.layers = layers;

        public override float[] Forward(float[] input) {
            var numLayers = layers.Length;
            
            for (var i = 0; i < numLayers; i++) input = layers[i].Forward(input);

            return input;
        }
    }
}