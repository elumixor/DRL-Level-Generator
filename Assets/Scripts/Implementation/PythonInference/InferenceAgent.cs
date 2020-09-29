using System.Linq;
using Common;
using DRL;
using DRL.Behaviours;
using Implementation.Dummy;
using PythonCommunication;
using NaughtyAttributes;
using UnityEngine;

namespace Implementation.PythonInference {
    public class InferenceAgent : Agent<DummyAction, State> {
        CyclingQueue<InferenceTransition> memory;
        [SerializeField, MinValue(1)] int memorySize;

        void Start() {
            Communicator.OpenConnection();
            memory = new CyclingQueue<InferenceTransition>(memorySize);
        }

        void OnDestroy() => Communicator.CloseConnection();

        public override void SaveTransition(Transition<DummyAction, State> transition) => memory.Push(new InferenceTransition(transition));

        public override DummyAction GetAction(State state) {
            var action = new DummyAction();
            var message = new Message(MessageHeader.Inference, state.ToBytes());
            action.AssignFromBytes(Communicator.Compute(message.ToBytes()));
            return action;
        }

        public override void OnEpisodeFinished() {
            if (memory.IsFull) Train();
        }


        void Train() =>
            Communicator.Compute(new Message(MessageHeader.Update, ByteConverter.ConcatBytes(memory.Length.ToBytes(), memory.ToBytes()))
                .ToBytes());
    }
}