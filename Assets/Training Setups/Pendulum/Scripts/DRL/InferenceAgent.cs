using BackendCommunication;
using DRL;
using DRL.Behaviours;
using Implementation.Dummy;
using Memory;
using NaughtyAttributes;
using UnityEngine;

namespace Training_Setups.Pendulum.Scripts.DRL {
    public class InferenceAgent : Agent<DummyAction, State> {
        [SerializeField, MinValue(1)] int memorySize;

        MemoryRRPB<Episode, InferenceTransition> memory;
        Episode currentEpisode = new Episode();

        void Start() {
            Communicator.OpenConnection();
            memory = new MemoryRRPB<Episode, InferenceTransition>(memorySize);
        }


        void OnDestroy() => Communicator.CloseConnection();

        public override void SaveTransition(Transition<DummyAction, State> transition) =>
            currentEpisode.Add(new InferenceTransition(transition));

        public override DummyAction GetAction(State state) {
            var action = new DummyAction();
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