using System.Linq;
using Common;
using Configuration.NN;
using NN;
using RL;
using Serialization;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts.RL
{
    public class Agent : MonoBehaviour, IAgent<State, Action>, INNAgent
    {
        Module actor;

        public Action GetAction(State state) => new Action(actor.Forward(state.AsEnumerable()).Softmax().Sample());

        /// <inheritdoc/>
        public void ConstructNN(Layout layout) { actor = new Sequential(layout.modules.Select(m => m.ToModule()).ToArray()); }

        /// <inheritdoc/>
        public void SetParameters(StateDict stateDict) { actor.LoadStateDict(stateDict); }
    }
}
