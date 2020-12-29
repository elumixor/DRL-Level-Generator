namespace Common.RandomValues
{
    public class EitherValue<T> : IRandomValue<T>
    {
        readonly T[] options;

        public EitherValue(T[] options) => this.options = options;

        /// <inheritdoc/>
        public T Sample => EitherValue.Get(options);
    }

    public static class EitherValue
    {
        public static T Get<T>(params T[] options) => options.RandomChoice();
    }
}
