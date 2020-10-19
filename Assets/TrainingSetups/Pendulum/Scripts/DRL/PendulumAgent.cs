using System.Linq;
using BackendCommunication;
using Configuration.NN;
using DRL;
using DRL.Behaviours;
using Memory;
using NaughtyAttributes;
using NN;
using Serialization;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class PendulumAgent : Agent<Action, State>, INNAgent {
        Episode currentEpisode = new Episode();

        MemoryRRPB<Episode, InferenceTransition> memory;
        [SerializeField, MinValue(1)] int memorySize;
        public Module NN { get; private set; }

        public void InitializeNN(Layout layout) => NN = new Sequential(layout.modules.Select(m => m.ToModule()).ToArray());

        void Start() { memory = new MemoryRRPB<Episode, InferenceTransition>(memorySize); }

        public override void SaveTransition(Transition<Action, State> transition) =>
            currentEpisode.Add(new InferenceTransition(transition));

        public override Action GetAction(State state) {
            var action = new Action();
            var (bytes, startIndex) = Communicator.Send(RequestType.SendTrainingData, state.ToBytes());
            action.AssignFromBytes(bytes, startIndex);
            return action;
        }

        public override void OnEpisodeFinished() {
            memory.Push(currentEpisode);
            currentEpisode = new Episode();
        }

        public override void OnEpochFinished() {
            if (memory.IsFull) Train();
        }

        void Train() => Communicator.Send(RequestType.SendTrainingData, memory.ToBytes());
    }
}