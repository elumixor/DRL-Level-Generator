using Common.ByteConversions;
using DRL;

namespace Memory {
    interface IMemory<in TEpisode, TTransition> : IByteConvertible
        where TTransition : IByteConvertible where TEpisode : IEpisode<TTransition> {
        bool IsFull { get; }
        void Push(TEpisode transition);
    }
}