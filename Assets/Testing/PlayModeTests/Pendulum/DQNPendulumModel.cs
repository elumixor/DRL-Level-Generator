using Common;
using NN;
using NN.Configuration;
using RemoteComputation.Models;
using RL;

namespace Testing.PlayModeTests.Pendulum
{
    public class DQNPendulumModel : LocalInferenceNN<Observation, Action>
    {
        new Sequential nn;
        const float EPSILON = 0.2f; // TODO: assign epsilon somehow dynamically and lower throughout the training
        public override ModelType ModelType { get; } = ModelType.DQN;

        const float DELTA_TIME = 0.16f;

        public override Action GetAction(Observation obs) =>
                MathExtensions.RandomValue() < EPSILON
                        ? new Action(MathExtensions.RandomValue() < 0.5f, DELTA_TIME)
                        : new Action(nn.Forward(obs).ArgMax()     == 0, DELTA_TIME);

        public override void AssignFromBytes(ByteReader reader)
        {
            Id = reader.ReadInt();
            nn = reader.Read<Sequential>();
            nn.LoadStateDict(reader.Read<StateDict>());
        }
    }
}
