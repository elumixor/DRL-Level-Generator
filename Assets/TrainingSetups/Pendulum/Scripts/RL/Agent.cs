using System.Collections.Generic;
using System.Linq;
using BackendCommunication;
using Common;
using Common.ByteConversions;
using Configuration.NN;
using NN;
using RL;
using Serialization;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.RL
{
    using Episode = List<Transition>;

    public class Agent : MonoBehaviour, IAgent<State, Action>, INNAgent
    {
        Module actor;
        Episode currentEpisode = new Episode();
        List<Episode> episodesInEpoch = new List<Episode>();

        public Action GetAction(State state) => new Action(actor.Forward(state.AsEnumerable()).Softmax().Sample());

        /// <inheritdoc/>
        public void ConstructNN(IEnumerable<ModuleConfiguration> modules) { actor = new Sequential(modules.Select(m => m.ToModule()).ToArray()); }

        /// <inheritdoc/>
        public void SetParameters(StateDict stateDict) { actor.LoadStateDict(stateDict); }

        public void OnTransition(State previousState, Action action, float reward, State nextState) =>
                currentEpisode.Add(new Transition(previousState, action, reward, nextState));

        public void OnEpisodeFinished()
        {
            episodesInEpoch.Add(currentEpisode);
            currentEpisode = new Episode();
        }

        public void OnEpochFinished()
        {
            var trainingData = episodesInEpoch.MapToBytes(episode => episode.MapToBytes(e => e.ToBytes()));
            var (data, startIndex) = Communicator.Send(RequestType.SendTrainingData, trainingData, 10000);
            var (stateDict, _)     = data.Get<StateDict>(startIndex);
            Debug.Log($"Received a state dict {stateDict}");
            actor.LoadStateDict(stateDict);
            episodesInEpoch = new List<Episode>();
        }
    }
}
