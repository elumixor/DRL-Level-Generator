using System.Collections.Generic;
using BackendCommunication;
using Common;
using Common.ByteConversions;
using NN;
using RLBehaviours;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts
{
    [RequireComponent(typeof(EnvironmentSettings))]
    public class Trainer : Trainer<State, int, Environment, Agent, Environment>
    {
        /// <inheritdoc/>
        protected override void Awake()
        {
            base.Awake();

            var settings = GetComponent<EnvironmentSettings>();

            foreach (var environmentInstance in environmentInstances) environmentInstance.settings = settings;
        }

        protected override void Train(List<List<(State state, int action, float reward, State nextState)>> epoch)
        {
            var trainingData = epoch.MapToBytes(episode => episode.MapToBytes(TransitionToBytes));
            var (data, startIndex) = Communicator.Send(RequestType.SendTrainingData, trainingData, 10000);
            var (stateDict, _)     = data.Get<StateDict>(startIndex);

            foreach (var environmentInstance in environmentInstances) environmentInstance.Agent.SetParameters(stateDict);
        }

        static IEnumerable<byte> TransitionToBytes((State state, int action, float reward, State nextState) transition)
        {
            var (state, action, reward, nextState) = transition;
            return state.ToBytes().ConcatMany(((float) action).ToBytes(), reward.ToBytes(), nextState.ToBytes());
        }
    }
}
