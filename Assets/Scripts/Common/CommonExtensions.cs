using System.Collections.Generic;

namespace Common {
    public static class CommonExtensions {
        public static int[] Copy(this int[] array) => (int[]) array.Clone();

        public static string FormString<T>(this IEnumerable<T> array, string separator = ", ", string openingBracket = "[",
                                           string closingBracket = "]") =>
            openingBracket + string.Join(separator, array) + closingBracket;
    }
}