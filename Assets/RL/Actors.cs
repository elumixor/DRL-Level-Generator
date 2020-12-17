using Common;
using NN;
using UnityEngine;

namespace RL
{
    public static class Actors
    {
        public static Vector DQN(this Module dqn, Vector state) => dqn.Forward(state).ArgMax();

        public static Vector DQN(this Module dqn, Vector state, float epsilonGreedy, int numActions) =>
                Random.value <= epsilonGreedy ? Random.Range(0, numActions) : dqn.Forward(state).ArgMax();

        public static Vector SampleLogits(this Module nn, Vector state) => nn.Forward(state).Softmax().Sample(); // todo don't softmax

        public static Vector SampleProbabilities(this Module nn, Vector state) => nn.Forward(state).Sample();
    }
}
