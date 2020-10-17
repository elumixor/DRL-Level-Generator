using BackendCommunication;
using DRL;
using DRL.Behaviours;
using Memory;
using NaughtyAttributes;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class InferenceAgent : Agent<Action, State> {
        [SerializeField, MinValue(1)] int memorySize;

        MemoryRRPB<Episode, InferenceTransition> memory;
        Episode currentEpisode = new Episode();

        void Start() { memory = new MemoryRRPB<Episode, InferenceTransition>(memorySize); }

        public override void SaveTransition(Transition<Action, State> transition) =>
            currentEpisode.Add(new InferenceTransition(transition));

        public override Action GetAction(State state) {
            var action = new Action();
            var message = new Message(MessageHeader.Inference, state.ToBytes());
            action.AssignFromBytes(Communicator.Compute(message.ToBytes()));
            return action;
        }

        public override void OnEpisodeFinished() {
            memory.Push(currentEpisode);
            currentEpisode = new Episode();
        }

        public override void OnEpochFinished() {
            if (memory.IsFull) Train();
        }

        void Train() => Communicator.Compute(new Message(MessageHeader.Update, memory.ToBytes()).ToBytes());
    }
}