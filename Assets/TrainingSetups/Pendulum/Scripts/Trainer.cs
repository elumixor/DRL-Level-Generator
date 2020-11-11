using System.Collections.Generic;
using RL.Common;
using RL.Common.ByteConversions;
using RL.RLBehaviours;

namespace TrainingSetups.Pendulum.Scripts
{
    public class Trainer : Trainer<State, int, Environment, Agent, Environment>
    {
        protected override IEnumerable<byte> TransitionToBytes((State state, int action, float reward, State nextState) transition)
        {
            var (state, action, reward, nextState) = transition;
            return state.ToBytes().ConcatMany(((float) action).ToBytes(), reward.ToBytes(), nextState.ToBytes());
        }
    }
}
