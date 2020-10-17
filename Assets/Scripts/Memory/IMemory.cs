using Common.ByteConversions;
using DRL;

namespace Memory {
    interface IMemory<in TEpisode, TTransition> : IByteConvertible
        where TTransition : IByteConvertible where TEpisode : IEpisode<TTransition> {
        void Push(TEpisode transition);
        bool IsFull { get; }
    }
}