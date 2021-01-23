using System.Collections.Generic;
using System.Linq;

namespace Common
{
    public static class EnumerableExtensions
    {
        public static IEnumerable<T> ConcatMany<T>(this IEnumerable<T> enumerable, params IEnumerable<T>[] enumerables)
        {
            return enumerable.Concat(enumerables.Aggregate((a, b) => a.Concat(b)));
        }
    }
}
