using System;
using Common.RandomValues;
using NUnit.Framework;

namespace Testing.EditorTests.NoUnity
{
    public class RandomValueTests
    {
        [Test]
        public void UniformValueTest()
        {
            for (var i = 0; i < 10; i++) Console.WriteLine(UniformValue.Get(-30f, 30f));
        }
    }
}
