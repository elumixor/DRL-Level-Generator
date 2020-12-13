// using System.Collections.Generic;
// using Common;
// using Common.ByteConversions;
// using RL.RLBehaviours;
//
// namespace TrainingSetups.Pendulum.Scripts
// {
//     public class Trainer : Trainer<Vector, int, Environment, Agent, Environment>
//     {
//         protected override IEnumerable<byte> TransitionToBytes((Vector state, int action, float reward, Vector nextState) transition)
//         {
//             var (state, action, reward, nextState) = transition;
//             return state.ToBytes().ConcatMany(((float) action).ToBytes(), reward.ToBytes(), nextState.ToBytes());
//         }
//     }
// }
