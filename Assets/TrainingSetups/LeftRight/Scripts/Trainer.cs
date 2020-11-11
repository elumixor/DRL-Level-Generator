using System.Collections.Generic;
using RL.Common;
using RL.Common.ByteConversions;
using RL.RLBehaviours;
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

        protected override IEnumerable<byte> TransitionToBytes((State state, int action, float reward, State nextState) transition)
        {
            var (state, action, reward, nextState) = transition;
            return state.ToBytes().ConcatMany(((float) action).ToBytes(), reward.ToBytes(), nextState.ToBytes());
        }
    }
}
