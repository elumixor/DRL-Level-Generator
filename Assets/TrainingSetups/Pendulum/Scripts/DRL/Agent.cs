using System.Collections.Generic;
using System.Linq;
using BackendCommunication;
using Common;
using Common.ByteConversions;
using Configuration.NN;
using DRL;
using DRL.Behaviours;
using NN;
using Serialization;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    using Episode = List<Transition>;

    public class Agent : Agent<Action, State>, INNAgent {
        Episode currentEpisode = new Episode();
        List<Episode> episodesInEpoch = new List<Episode>();

        Module actor;

        public void InitializeNN(Layout layout, StateDict stateDict) {
            actor = new Sequential(layout.modules.Select(m => m.ToModule()).ToArray());
            actor.LoadStateDict(stateDict);
        }

        public override Action GetAction(State state) => new Action(actor.Forward(state.AsEnumerable()).Softmax().Sample());

        public override void OnTransition(State previousState, Action action, float reward, State nextState) =>
            currentEpisode.Add(new Transition(previousState, action, reward, nextState));

        public override void OnEpisodeFinished() {
            episodesInEpoch.Add(currentEpisode);
            currentEpisode = new Episode();
        }

        public override void OnEpochFinished() {
            var trainingData = episodesInEpoch.MapToBytes(episode => episode.MapToBytes(e => e.ToBytes()));
            var (data, startIndex) = Communicator.Send(RequestType.SendTrainingData, trainingData, 10000);
            var (stateDict, _) = data.Get<StateDict>(startIndex);
            Debug.Log($"Received a state dict {stateDict}");
            actor.LoadStateDict(stateDict);
            episodesInEpoch = new List<Episode>();
        }
    }
}