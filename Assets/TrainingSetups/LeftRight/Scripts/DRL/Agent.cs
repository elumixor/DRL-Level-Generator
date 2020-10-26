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

namespace TrainingSetups.LeftRight.Scripts.DRL {
    using Episode = List<Transition>;

    public class Agent : Agent<Action, State>, INNAgent {
        // For visualization, is not exposed to the agent while inference or training
        public float bigRewardPosition;
        public float smallRewardPosition;
        Module actor;
        Episode currentEpisode = new Episode();
        List<Episode> episodesInEpoch = new List<Episode>();

        void OnDrawGizmos() {
            // position
            Gizmos.color = new Color(1f, 0.59f, 0.37f);
            Gizmos.DrawSphere(transform.position, .5f);

            // probabilities
            Gizmos.color = new Color(0.64f, 0.9f, 0.73f);
            const float step = .1f;
            for (var x = -bigRewardPosition; x < smallRewardPosition; x += step) {
                var pLeft = actor.Forward(x.Yield()).Softmax().First();
                Gizmos.DrawCube(new Vector3(x, 0, pLeft * .5f), new Vector3(step, 0, pLeft));
            }
        }


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