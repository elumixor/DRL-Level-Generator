using System.Collections.Generic;
using System.Linq;
using Common;
using DRL;
using DRL.Behaviours;
using Implementation.Dummy;
using PythonCommunication;
using NaughtyAttributes;
using UnityEngine;

namespace Implementation.PythonInference {
    using Episode = List<InferenceTransition>;

    public class InferenceAgent : Agent<DummyAction, State> {
        [SerializeField, MinValue(1)] int memorySize;

        CyclingQueue<Episode> episodes;
        Episode currentEpisode = new Episode();


        void Start() {
            Communicator.OpenConnection();
            episodes = new CyclingQueue<Episode>(memorySize);
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
            episodes.Push(currentEpisode);
            currentEpisode = new Episode();
        }

        public override void OnEpochFinished() => Train();

        byte[] TrainingDataAsBytes => ByteConverter.ConcatBytes(episodes.Length.ToBytes(), episodes.Select(EpisodeToBytes).ToBytes());

        static byte[] EpisodeToBytes(Episode episode) => ByteConverter.ConcatBytes(episode.Count.ToBytes(), episode.ToBytes());

        void Train() =>
            Communicator.Compute(new Message(MessageHeader.Update, TrainingDataAsBytes).ToBytes());
    }
}