using BackendCommunication;
using DRL;
using DRL.Behaviours;
using Memory;
using NaughtyAttributes;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class InferenceAgent : Agent<Action, State> {
        Episode currentEpisode = new Episode();

        MemoryRRPB<Episode, InferenceTransition> memory;
        [SerializeField, MinValue(1)] int memorySize;

        void Start() { memory = new MemoryRRPB<Episode, InferenceTransition>(memorySize); }

        public override void SaveTransition(Transition<Action, State> transition) =>
            currentEpisode.Add(new InferenceTransition(transition));

        public override Action GetAction(State state) {
            var action = new Action();
            var (bytes, _, startIndex) = Communicator.Send(RequestType.Inference, state.ToBytes());
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

        void Train() => Communicator.Send(RequestType.Update, memory.ToBytes());
    }
}