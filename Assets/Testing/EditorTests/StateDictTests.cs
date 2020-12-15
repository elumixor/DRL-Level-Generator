// using System.Linq;
// using NUnit.Framework;
// using RL;
// using RL.Common.ByteConversions;
// using RL.NN;
//
// namespace Testing.EditorTests
// {
//     public class StateDictTests
//     {
//         [Test]
//         public void CreatingFromLinearWorks()
//         {
//             var linear = new Linear(5, 4);
//             var sd = linear.StateDict;
//
//             Assert.IsEmpty(sd.childParameters);
//             Assert.IsNotEmpty(sd.selfParameters);
//
//             Assert.IsInstanceOf<Tensor>(sd.selfParameters[ModuleParameterName.weight]);
//             Assert.IsInstanceOf<Tensor>(sd.selfParameters[ModuleParameterName.bias]);
//
//             Assert.AreEqual(sd.selfParameters[ModuleParameterName.bias].shape, new[] {4});
//             Assert.AreEqual(sd.selfParameters[ModuleParameterName.weight].shape, new[] {4, 5});
//         }
//
//         [Test]
//         public void CreatingFomSequentialWorks()
//         {
//             var sequential = new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2));
//             var sd = sequential.StateDict;
//
//             Assert.IsNotEmpty(sd.childParameters);
//             Assert.IsEmpty(sd.selfParameters);
//
//             Assert.AreEqual(4, sd.Length);
//         }
//
//         [Test]
//         public void CreatingFomNestedSequentialWorks()
//         {
//             var sequential = new Sequential(new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                             new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                             new Linear(4, 2));
//             var sd = sequential.StateDict;
//             Assert.IsNotEmpty(sd.childParameters);
//             Assert.IsEmpty(sd.selfParameters);
//
//             Assert.AreEqual(5 * 2, sd.Length);
//         }
//
//         [Test]
//         public void AssigningSameStateDictCreatesEqualLinearModules()
//         {
//             var l1 = new Linear(5, 4);
//             var l2 = new Linear(5, 4);
//
//             Assert.AreNotEqual(l1, l2);
//
//             var sd = l1.StateDict;
//             l2.LoadStateDict(sd);
//
//             Assert.AreEqual(l1, l2);
//         }
//
//         [Test]
//         public void AssigningSameStateDictCreatesEqualSequentialModules()
//         {
//             var s1 = new Sequential(new Linear(1, 10), new ReLU(), new Linear(4, 2));
//             var s2 = new Sequential(new Linear(1, 10), new ReLU(), new Linear(4, 2));
//
//             Assert.AreNotEqual(s1, s2);
//
//             var sd = s1.StateDict;
//             s2.LoadStateDict(sd);
//
//             Assert.AreEqual(s1, s2);
//         }
//
//         [Test]
//         public void AssigningSameStateDictCreatesEqualNestedSequentialModules()
//         {
//             var s1 = new Sequential(new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                     new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                     new Linear(4, 2));
//             var s2 = new Sequential(new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                     new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                     new Linear(4, 2));
//
//             Assert.AreNotEqual(s1, s2);
//
//             var sd = s1.StateDict;
//             s2.LoadStateDict(sd);
//
//             Assert.AreEqual(s1, s2);
//         }
//
//         // Byte serialization
//         [Test]
//         public void SerializationOfStateDictWorks()
//         {
//             var l1 = new Linear(4, 5);
//             var sd = l1.StateDict;
//             var bytes = sd.ToBytes().ToArray();
//             var sd2 = bytes.Get<StateDict>().result;
//             Assert.AreEqual(sd, sd2);
//         }
//
//         [Test]
//         public void SerializationOfNestedStateDictWorks()
//         {
//             var s = new Sequential(new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                    new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
//                                    new Linear(4, 2));
//             var sd = s.StateDict;
//             var bytes = sd.ToBytes().ToArray();
//             var sd2 = bytes.Get<StateDict>().result;
//             Assert.AreEqual(sd, sd2);
//         }
//     }
// }


