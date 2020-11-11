using System.Linq;
using RL.Common;
using RL.NN;
using RL.RL;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts
{
    public class Agent : MonoBehaviour, IAgent<State, int>, INNAgent
    {
        Module actor;
        public int GetAction(State state) => actor.Forward(state.AsEnumerable()).Softmax().Sample();

        /// <inheritdoc/>
        public void InitializeNN(Module nn) { actor = nn; }

        /// <inheritdoc/>
        public void SetParameters(StateDict stateDict) => actor.LoadStateDict(stateDict);
    }
}
