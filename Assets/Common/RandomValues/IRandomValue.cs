namespace Common.RandomValues
{
    public interface IRandomValue<T>
    {
        T Sample { get; }
    }

    public interface IRandomValue : IRandomValue<float> { }
}
