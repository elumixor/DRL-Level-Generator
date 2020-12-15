using System.Linq;
using Common;
using NN;
using NN.Configuration;
using RemoteComputation.Models;
using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class DQNPendulumActor : LocalInferenceNN
    {
        int numActions;
        float epsilon;
        public override ModelType ModelType { get; } = ModelType.DQN;

        public override Vector GetAction(Vector state) =>
                Random.value < epsilon ? new Vector(Random.Range(0, numActions)) : nn.Forward(state).ArgMax();

        public override void AssignFromBytes(ByteReader reader)
        {
            Id = reader.ReadInt();
            var sequential = reader.Read<Sequential>();
            nn = sequential;
            nn.LoadStateDict(reader.Read<StateDict>());
            epsilon = reader.ReadFloat();

            foreach (var layer in sequential.Layers.Reverse())
                if (layer is IFixedOutputLayer fixedOutputLayer) {
                    numActions = fixedOutputLayer.OutputSize;
                    break;
                }
        }
    }
}
