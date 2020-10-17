using Common.ByteConversions;

namespace DRL {
    public interface IEpisode<in TTransition> where TTransition : IByteConvertible {
        float TotalReward { get; }
        int Length { get; }
        void Add(TTransition transition);
    }
}