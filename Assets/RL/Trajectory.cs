using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;

namespace RL
{
    public class Trajectory : IByteConvertible
    {
        List<Transition> transitions;

        public int Length => transitions.Count;

        public void Add(Transition transition) => transitions.Add(transition);

        public void Add(Vector state, Vector action, float reward, Vector nextState) => Add(new Transition(state, action, reward, nextState));

        public IEnumerable<byte> Bytes => Length.ToBytes().ConcatMany(transitions.Select(transition => transition.Bytes).ToArray());
    }
}
