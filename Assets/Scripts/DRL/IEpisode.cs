using Common;

namespace DRL {
    public interface IEpisode<TTransition> : IByteConvertible where TTransition : IByteConvertible {
        void Add(TTransition transition);
        float TotalReward { get; }
        int Length { get; }
    }
}