using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using Common;

namespace NN {
    public class Sequential : Module {
        readonly Module[] layers;
        public Sequential(params Module[] layers) => this.layers = layers;

        public override float[] Forward(float[] input) {
            var numLayers = layers.Length;

            for (var i = 0; i < numLayers; i++) input = layers[i].Forward(input);

            return input;
        }

        public override void LoadStateDict(StateDict stateDict) {
            var parameters = stateDict.childParameters;
            foreach (var (path, (name, value)) in parameters)
                SetParameter(path, name, value);
        }

        void SetParameter(IEnumerable<int> path, ModuleParameterName name, Tensor value) {
            Module layer = this;

            foreach (var i in path)
                if (layer is Sequential sequential)
                    layer = sequential.layers[i];
                else
                    throw new SerializationException($"Trying to get a child [{i}] of a module {layer}, but it is not a Sequential");

            layer.SetParameter(name, value);
        }

        StateDict GetStateDict(int[] currentPath) {
            var childParameters = new List<(int[] path, (ModuleParameterName name, Tensor value) parameter)>();
            var nextPath = new int[currentPath.Length + 1];
            Array.Copy(currentPath, nextPath, currentPath.Length);

            for (var i = 0; i < layers.Length; i++) {
                var layer = layers[i];
                nextPath[currentPath.Length] = i;
                var childDict = layer is Sequential sequential ? sequential.GetStateDict(nextPath) : layer.GetStateDict();

                childParameters.AddRange(childDict.selfParameters.Select(parameter => (nextPath.Copy(), (parameter.Key, parameter.Value))));
                childParameters.AddRange(childDict.childParameters);
            }

            return new StateDict(childParameters);
        }

        public override StateDict GetStateDict() => GetStateDict(new int[0]);

        bool Equals(Sequential other) {
            if (layers.Length != other.layers.Length) return false;

            return !layers.Where((t, i) => !Equals(t, other.layers[i])).Any();
        }

        public override bool Equals(object obj) {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            return obj.GetType() == GetType() && Equals((Sequential) obj);
        }
    }
}