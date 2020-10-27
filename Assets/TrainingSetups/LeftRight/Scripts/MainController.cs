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
    public class MainController : MainController<State, Action, EnvironmentInstance, Agent, EnvironmentInstance>
    {
        /// <inheritdoc/>
        protected override void Awake()
        {
            base.Awake();

            var settings = GetComponent<EnvironmentSettings>();

            foreach (var trainingInstance in trainingInstances) trainingInstance.settings = settings;
        }

        protected override void Train(List<List<(State state, Action action, float reward, State nextState)>> epoch)
        {
            var trainingData = epoch.MapToBytes(episode => episode.MapToBytes(TransitionToBytes));
            var (data, startIndex) = Communicator.Send(RequestType.SendTrainingData, trainingData, 10000);
            var (stateDict, _)     = data.Get<StateDict>(startIndex);

            foreach (var trainingInstance in trainingInstances) trainingInstance.Agent.SetParameters(stateDict);
        }

        static IEnumerable<byte> TransitionToBytes((State state, Action action, float reward, State nextState) transition)
        {
            var (state, action, reward, nextState) = transition;
            return state.ToBytes().ConcatMany(action.X.ToBytes(), reward.ToBytes(), nextState.ToBytes());
        }
    }
}
