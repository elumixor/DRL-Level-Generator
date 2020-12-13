// using System.Collections.Generic;
// using RL.Common;
// using RL.Common.ByteConversions;
// using RL.RLBehaviours;
// using UnityEngine;
//
// namespace TrainingSetups.LeftRight.Scripts
// {
//     [RequireComponent(typeof(EnvironmentSettings))]
//     public class Trainer : Trainer<Vector, int, Environment, Agent, Environment>
//     {
//         /// <inheritdoc/>
//         protected override void Awake()
//         {
//             base.Awake();
//
//             var settings = GetComponent<EnvironmentSettings>();
//
//             foreach (var environmentInstance in environmentInstances) environmentInstance.settings = settings;
//         }
//
//         protected override IEnumerable<byte> TransitionToBytes((Vector state, int action, float reward, Vector nextState) transition)
//         {
//             var (state, action, reward, nextState) = transition;
//             return state.ToBytes().ConcatMany(((float) action).ToBytes(), reward.ToBytes(), nextState.ToBytes());
//         }
//     }
// }
