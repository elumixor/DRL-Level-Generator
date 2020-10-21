using System.Collections.Generic;
using System.Linq;
using BackendCommunication;
using Common.ByteConversions;
using Configuration.NN;
using DRL;
using DRL.Behaviours;
using NN;
using Serialization;

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

        public override Action GetAction(State state) => new Action(actor.Forward(state.AsEnumerable()));

        public override void OnTransition(State previousState, Action action, float reward, State nextState) =>
            currentEpisode.Add(new Transition(previousState, action, reward, nextState));

        public override void OnEpisodeFinished() {
            episodesInEpoch.Add(currentEpisode);
            currentEpisode = new Episode();
        }

        public override void OnEpochFinished() {
            var trainingData = episodesInEpoch.MapToBytes(episode => episode.MapToBytes(e => e.ToBytes()));
            var (data, startIndex) = Communicator.Send(RequestType.SendTrainingData, trainingData);
            var (stateDict, _) = data.Get<StateDict>(startIndex);
            actor.LoadStateDict(stateDict);
            episodesInEpoch = new List<Episode>();
        }
    }
}