using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;
using NUnit.Framework;
using UnityEngine;

namespace Testing.EditorTests {
    public class SerializationTests {
        [Test] public void CanConvertSimpleTypes() {
            Assert.AreEqual(5.0f, 5.0f.ToBytes().ToArray().ToFloat());
            Assert.AreEqual(5, 5.ToBytes().ToArray().ToInt());
            Assert.AreEqual(true, true.ToBytes().ToArray().ToBool());
            Assert.AreEqual(false, false.ToBytes().ToArray().ToBool());
            const string str = "hello world с утфčaraktёрщі";
            var (result, readCount) = str.ToBytes().ToArray().GetString();
            Assert.AreEqual(str, result);
        }

        [Test] public void CanConvertEnum() {
            Assert.AreEqual(MyEnum.HelloWorld.ToString(), nameof(MyEnum.HelloWorld));
            var success = Enum.TryParse("GoodbyeWorld", out MyEnum result);
            Assert.IsTrue(success);
            Assert.AreEqual(result, MyEnum.GoodbyeWorld);
            var failure = Enum.TryParse("Nothing", out result);
            Assert.IsFalse(failure);
            Assert.AreNotEqual(result, MyEnum.GoodbyeWorld);
        }

        [Test] public void CanConvertUnityTypes() {
            Assert.AreEqual(new Vector2(5, 6), new Vector2(5, 6).ToBytes().ToArray().ToVector2());
            Assert.AreEqual(new Vector3(5, 6, 7), new Vector3(5, 6, 7).ToBytes().ToArray().ToVector3());
        }

        [Test] public void CanConvertWithOffset() {
            var bytes = 5.ToBytes().ConcatMany(6.ToBytes(), new Vector2(7, 8).ToBytes(), 9.ToBytes(), new Vector3(1, 2, 3).ToBytes())
                         .ToArray();

            var v2 = bytes.ToVector2(sizeof(int)                                   + sizeof(int));
            var v3 = bytes.ToVector3(sizeof(int) + sizeof(int) + 2 * sizeof(float) + sizeof(int));

            Assert.AreEqual(new Vector2(7, 8), v2);
            Assert.AreEqual(new Vector3(1, 2, 3), v3);
        }

        [Test] public void CanConvertCustomType() {
            var c = new C {f1 = 5, v2 = new Vector2(6, 7), v3 = new Vector3(8, 9)};
            var c2 = new C();
            var size = c2.AssignFromBytes(c.ToBytes().ToArray());
            Assert.AreEqual(c, c2);
            Assert.AreEqual(size, sizeof(float) * (1 + 2 + 3));
        }


        [Test] public void CanConvertArray() {
            var floatList = new float[] {1, 2, 3, 4, 5};
            var serialized = floatList.ToBytes(floatList.Length).ToArray();
            var length = serialized.ToInt();
            Assert.AreEqual(length, floatList.Length);

            for (var i = 0; i < length; i++) {
                var item = serialized.ToFloat(sizeof(int) + i * sizeof(float));
                Assert.AreEqual(floatList[i], item);
            }
        }

        [Test] public void CanConvertCustomClassList() {
            var list = new List<C> {
                new C {f1 = 1, v2 = new Vector2(2, 3), v3 = new Vector3(4, 5, 6)},
                new C {f1 = 2, v2 = new Vector2(3, 4), v3 = new Vector3(5, 6, 8)},
                new C {f1 = 3, v2 = new Vector2(4, 5), v3 = new Vector3(6, 7, 9)},
            };
            var serialized = list.ToBytes(list.Count).ToArray();
            var length = serialized.ToInt();

            Assert.AreEqual(length, list.Count);
            var (reconstructed, newOffset) = serialized.GetList<C>();

            for (var i = 0; i < length; i++) Assert.AreEqual(list[i], reconstructed[i]);

            Assert.AreEqual(newOffset, sizeof(int) + sizeof(float) * 3 * (1 + 2 + 3));
        }

        [Test] public void CanSerializeTensor() {
            var tensor = new Tensor(new float[] {1, 2, 3, 4, 5, 6}, new[] {2, 3});
            var serialized = tensor.ToBytes().ToArray();
            Console.WriteLine(serialized.FormString());
            var (reconstructed, bytes_read) = serialized.Get<Tensor>();
            Assert.AreEqual(tensor, reconstructed);
        }

        enum MyEnum {
            HelloWorld,
            GoodbyeWorld,
        }

        class C : IByteSerializable {
            public float f1;
            public Vector2 v2;
            public Vector3 v3;

            public IEnumerable<byte> ToBytes() => f1.ToBytes().ConcatMany(v2.ToBytes(), v3.ToBytes());

            public int AssignFromBytes(byte[] bytes, int startIndex = 0) {
                f1 = bytes.ToFloat(startIndex);
                v2 = bytes.ToVector2(startIndex                                 + sizeof(float));
                v3 = bytes.ToVector3(startIndex + sizeof(float) + sizeof(float) + sizeof(float));
                return sizeof(float) * (1 + 2 + 3);
            }

            bool Equals(C other) => f1.Equals(other.f1) && v2 == other.v2 && v3 == other.v3;

            public override bool Equals(object obj) {
                if (ReferenceEquals(null, obj)) return false;
                if (ReferenceEquals(this, obj)) return true;
                return obj.GetType() == GetType() && Equals((C) obj);
            }

            public override int GetHashCode() {
                unchecked {
                    var hashCode = f1.GetHashCode();
                    hashCode = (hashCode * 397) ^ v2.GetHashCode();
                    hashCode = (hashCode * 397) ^ v3.GetHashCode();
                    return hashCode;
                }
            }
        }
    }
}