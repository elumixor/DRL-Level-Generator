using System;
using DRL.Behaviours;
using Implementation.Dummy;
using PythonCommunication;
using Utilities;
using NaughtyAttributes;

namespace Implementation.PythonInference {
    [RequireComponent(typeof(PlayerBehaviourController))]
    public class InferenceAgent : Agent<DummyAction, DummyObservation> {
        MemoryBuffer<DummyAction, State> memory;
        [SerializeField, MinValue(1)] int memorySize;

        private PlayerBehaviourController player;
        
        void Start() {
            Communicator.OpenConnection();
            memory = new MemoryBuffer<DummyAction, State>(memorySize);
            player = GetComponent<PlayerBehaviourController>();
        }
        
        void OnDestroy() { Communicator.CloseConnection(); }

        public override void SaveStep(DummyObservation observation, DummyAction action, float reward) {
            memory.Push(CreateStateFromObservation(observation), action, reward)
        }

        public override DummyAction GetAction(DummyObservation observation) {
            var action = new DummyAction();
            action.AssignFromBytes(Communicator.Compute(CreateInferenceMessage(observation).ToBytes()));
            return action;
        }

        public override void OnEpisodeFinished() {
            if (memory.IsFull) Train();
        }

        State CreateStateFromObservation(DummyObservation observation) {
            return new State(
                FindObjectsOfType<Enemy>()
                    .Select(e => (Vector2)e.transform.position)
                    .ToArray(), 
                (Vector2)player.Position, player.Angle, player.AnglularSpeed
            player.UpwardSpeed);
        } 

        void Train() {
            Communicator.Compute(new Message(MessageHeader.Training, memory.ToBytes()));
        }

        static Message CreateInferenceMessage(DummyObservation observation) => new Message(MessageHeader.Inference, observation.ToBytes());
    }
}