using System;
using DRL.Behaviours;
using Implementation.Dummy;
using PythonCommunication;
using Utilities;

namespace Implementation.PythonInference {
    public class InferenceAgent : Agent<DummyAction, DummyObservation> {
        void Start() { Communicator.OpenConnection(); }
        void OnDestroy() { Communicator.CloseConnection(); }

        MemoryBuffer<DummyAction, DummyObservation> memory = new MemoryBuffer<DummyAction, DummyObservation>();

        public override void SaveStep(DummyObservation previousObservation, DummyAction action, float reward) { }

        public override DummyAction GetAction(DummyObservation observation) {
            var action = new DummyAction();
            action.AssignFromBytes(Communicator.Compute(CreateInferenceMessage(observation).ToBytes()));
            return action;
        }

        public override void OnEpisodeFinished() {
            if (memory.IsFull) Train();
        }

        void Train() {
            memory.ToBytes();
        }

        static Message CreateInferenceMessage(DummyObservation observation) => new Message(MessageHeader.Inference, observation.ToBytes());
    }
}