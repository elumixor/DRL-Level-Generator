using System.Linq;
using Common;
using NN;
using NN.Configuration;
using RemoteComputation.Models;
using RL;
using UnityEngine;

namespace Testing.PlayModeTests.Pendulum
{
    public class DQNPendulumModel : LocalInferenceNN<State, Action>
    {
        new Sequential nn;
        int numActions;
        readonly float epsilon = 0.2f; // TODO: assign epsilon somehow dynamically and lower throughout the training
        public override ModelType ModelType { get; } = ModelType.DQN;

        public override Action GetAction(State state) =>
                MathExtensions.RandomValue() < epsilon ? new Action(MathExtensions.RandomValue() < 0.5f) : new Action(nn.Forward(state).ArgMax() == 0);

        public override void AssignFromBytes(ByteReader reader)
        {
            Id = reader.ReadInt();
            nn = reader.Read<Sequential>();
            nn.LoadStateDict(reader.Read<StateDict>());

            // epsilon = reader.ReadFloat();

            foreach (var layer in nn.Layers.Reverse())
                if (layer is IFixedOutputLayer fixedOutputLayer) {
                    numActions = fixedOutputLayer.OutputSize;
                    break;
                }
        }
    }
}
