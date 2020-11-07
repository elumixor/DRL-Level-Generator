using System.Collections.Generic;

namespace Common
{
    public static class CommonExtensions
    {
        public static int[] Copy(this int[] array) => (int[]) array.Clone();

        public static string MakeString<T>(this IEnumerable<T> array, string separator = ", ", string openingBracket = "[", string closingBracket = "]") =>
                openingBracket + string.Join(separator, array) + closingBracket;

        // Yields a single item as enumerable
        public static IEnumerable<T> Yield<T>(this T item) { yield return item; }

        public static bool IsEmpty<T>(this IReadOnlyCollection<T> collection) => collection.Count    == 0;
        public static bool IsNotEmpty<T>(this IReadOnlyCollection<T> collection) => collection.Count != 0;
    }
}
