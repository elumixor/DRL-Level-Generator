﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using Common;
using Common.ByteConversions;
using Common.Exceptions;
using NN.Configuration;

// using UnityEngine;

namespace NN
{
    public class Sequential : Module, IByteAssignable
    {
        public Module[] Layers { get; private set; }
        public Sequential() { }
        public Sequential(params Module[] layers) => Layers = layers;
        public Sequential(IEnumerable<Module> layers) => Layers = layers.ToArray();

        public override StateDict StateDict => GetStateDict(new int[0]);

        public override IEnumerable<float> Forward(IEnumerable<float> input) =>
                Layers.Aggregate(input, (current, layer) => layer.Forward(current));

        public override void LoadStateDict(StateDict stateDict)
        {
            var parameters = stateDict.childParameters;
            foreach (var (path, (name, value)) in parameters) SetParameter(path, name, value);
        }

        void SetParameter(IEnumerable<int> path, ModuleParameterName name, Tensor value)
        {
            Module layer = this;

            foreach (var i in path)
                if (layer is Sequential sequential)
                    layer = sequential.Layers[i];
                else
                    throw new SerializationException($"Trying to get a child [{i}] of a module {layer}, but it is not a Sequential");

            layer.SetParameter(name, value);
        }

        StateDict GetStateDict(int[] currentPath)
        {
            var childParameters = new List<(int[] path, (ModuleParameterName name, Tensor value) parameter)>();
            var nextPath = new int[currentPath.Length + 1];
            Array.Copy(currentPath, nextPath, currentPath.Length);

            for (var i = 0; i < Layers.Length; i++) {
                var layer = Layers[i];
                nextPath[currentPath.Length] = i;
                var childDict = layer is Sequential sequential ? sequential.GetStateDict(nextPath) : layer.StateDict;

                childParameters.AddRange(childDict.selfParameters.Select(parameter => (nextPath.Copy(), (parameter.Key, parameter.Value))));
                childParameters.AddRange(childDict.childParameters);
            }

            return new StateDict(childParameters);
        }

        bool Equals(Sequential other)
        {
            if (Layers.Length != other.Layers.Length) return false;

            return !Layers.Where((t, i) => !Equals(t, other.Layers[i])).Any();
        }

        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;

            return obj.GetType() == GetType() && Equals((Sequential) obj);
        }

        /// <inheritdoc/>
        public void AssignFromBytes(ByteReader reader)
        {
            var layersCount = reader.ReadInt();
            Layers = new Module[layersCount];

            for (var i = 0; i < layersCount; i++) {
                var layerType = (ModuleLayerName) reader.ReadInt();

                switch (layerType) {
                    case ModuleLayerName.Linear:
                        Layers[i] = new Linear(reader.ReadInt(), reader.ReadInt());
                        break;
                    case ModuleLayerName.ReLU:
                        Layers[i] = new ReLU();
                        break;
                    case ModuleLayerName.Softmax:
                        Layers[i] = new Softmax();
                        break;
                    case ModuleLayerName.Sequential: throw new BaseException("Nested sequential layers are not supported");
                    default:                         throw new ArgumentOutOfRangeException();
                }
            }
        }

        /// <inheritdoc/>
        public override string ToString()
        {
            var builder = new StringBuilder($"Sequential ({Layers.Length})\n");

            foreach (var layer in Layers)
                if (layer is Linear linear)
                    builder.AppendLine($"\t{layer} ({linear.InputSize} -> {linear.OutputSize})");
                else
                    builder.AppendLine($"\t{layer}");

            return builder.ToString();
        }
    }
}
