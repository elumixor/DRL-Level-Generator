using System.Collections.Generic;
using System.Linq;
using Common;
using Configuration.NN;
using NN;
using RL;
using Serialization;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts
{
    public class Agent : MonoBehaviour, IAgent<State, int>, INNAgent
    {
        Module actor;

        public int GetAction(State state) => actor.Forward(state.AsEnumerable()).Softmax().Sample();

        /// <inheritdoc/>
        public void ConstructNN(IEnumerable<ModuleConfiguration> modules) { actor = new Sequential(modules.Select(m => m.ToModule()).ToArray()); }

        /// <inheritdoc/>
        public void SetParameters(StateDict stateDict)
        {
            actor.LoadStateDict(stateDict);
            Debug.Log("Agent updated");
            Debug.Log(actor.Forward(1f.Yield()).ToArray().MakeString());
        }
    }
}
