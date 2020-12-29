using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;

namespace RL
{
    public class Trajectory<TState, TAction, TObservation> : IByteConvertible, IReadOnlyList<Transition<TState, TAction, TObservation>>
            where TState : ObservableState<TObservation>, IByteConvertible
            where TAction : Vector
            where TObservation : Vector

    {
        readonly List<Transition<TState, TAction, TObservation>> transitions = new List<Transition<TState, TAction, TObservation>>();

        public int Count => transitions.Count;

        /// <inheritdoc/>
        public Transition<TState, TAction, TObservation> this[int index] => transitions[index];

        public void Add(Transition<TState, TAction, TObservation> transition) => transitions.Add(transition);

        public void Add(TState state, TAction action, float reward, TState nextState) =>
                Add(new Transition<TState, TAction, TObservation>(state, action, reward, nextState));

        public IEnumerable<byte> Bytes => Count.ToBytes().ConcatMany(transitions.Select(transition => transition.Bytes).ToArray());

        /// <inheritdoc/>
        public IEnumerator<Transition<TState, TAction, TObservation>> GetEnumerator() =>
                ((IEnumerable<Transition<TState, TAction, TObservation>>) transitions).GetEnumerator();

        /// <inheritdoc/>
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }

    public class Trajectory : Trajectory<Vector, Vector, Vector> { }
}
