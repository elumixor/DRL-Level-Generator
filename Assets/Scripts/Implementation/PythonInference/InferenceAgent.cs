using System;
using DRL.Behaviours;
using Implementation.Dummy;
using PythonCommunication;

namespace Implementation.PythonInference {
    public class InferenceAgent : Agent<DummyAction, DummyObservation> {
        void Start() { Communicator.OpenConnection(); }
        void OnDestroy() { Communicator.CloseConnection(); }

        public override DummyAction GetAction(DummyObservation observation) {
            var action = new DummyAction();
            action.AssignFromBytes(Communicator.Compute(CreateInferenceMessage(observation).ToBytes()));
            return action;
        }

        static Message CreateInferenceMessage(DummyObservation observation) => new Message(MessageHeader.Inference, observation.ToBytes());
    }
}