using System.Linq;
using Common;
using DRL.Behaviours;
using Implementation.Dummy;
using PythonCommunication;
using Utilities;
using NaughtyAttributes;
using Player;
using UnityEditor;
using UnityEngine;

namespace Implementation.PythonInference {
    [RequireComponent(typeof(PlayerBehaviouralController))]
    public class InferenceAgent : Agent<DummyAction, Observation> {
        MemoryBuffer<DummyAction, State> memory;
        [SerializeField, MinValue(1)] int memorySize;

        PlayerBehaviouralController player;

        void Start() {
            Communicator.OpenConnection();
            memory = new MemoryBuffer<DummyAction, State>(memorySize);
            player = GetComponent<PlayerBehaviouralController>();
        }

        void OnDestroy() => Communicator.CloseConnection();

        public override void SaveStep(Observation observation, DummyAction action, float reward) =>
            memory.Push(CreateStateFromObservation(observation), action, reward);

        public override DummyAction GetAction(Observation observation) {
            var action = new DummyAction();
            var message = new Message(MessageHeader.Inference, CreateStateFromObservation(observation).ToBytes());
            action.AssignFromBytes(Communicator.Compute(message.ToBytes()));
            return action;
        }

        public override void OnEpisodeFinished() {
            if (memory.IsFull) Train();
        }

        State CreateStateFromObservation(Observation observation) =>
            new State(observation.enemiesPositions, observation.playerPosition, player.Angle, player.AngularSpeed, player.UpwardSpeed);

        void Train() => Communicator.Compute(new Message(MessageHeader.Update, memory.ToBytes()).ToBytes());
    }
}