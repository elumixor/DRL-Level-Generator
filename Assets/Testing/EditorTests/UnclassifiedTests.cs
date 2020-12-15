// using System.Linq;
// using NUnit.Framework;
// using RL.Common;
// using UnityEngine;
//
// namespace Testing.EditorTests
// {
//     public class UnclassifiedTests
//     {
//         [Test]
//         public void SamplingTestEqual()
//         {
//             var probs = new[] {.5f, .5f};
//
//             var mean = 0f;
//             const int count = 1000000;
//             for (var i = 0; i < count; i++) mean += probs.Sample();
//
//             mean /= count;
//
//             Assert.AreEqual(.5f, mean, 0.01f);
//             Debug.Log(.5f);
//             Debug.Log(mean);
//         }
//
//         [Test]
//         public void SamplingTestDifferent()
//         {
//             const float p = .2f;
//             var probs = new[] {1f - p, p};
//
//             var mean = 0f;
//             const int count = 1000000;
//             for (var i = 0; i < count; i++) mean += probs.Sample();
//
//             mean /= count;
//
//             Assert.AreEqual(p, mean, 0.01f);
//             Debug.Log(p);
//             Debug.Log(mean);
//         }
//
//         [Test]
//         public void SoftmaxTest()
//         {
//             var sm = new[] {1f, 2f}.Softmax().ToArray();
//             Assert.AreEqual(.2689, sm[0], 1e-4f);
//             Assert.AreEqual(.7311, sm[1], 1e-4f);
//         }
//     }
// }


