using NUnit.Framework;
using Serialization;
using UnityEngine;

namespace Testing.EditorTests {
    public class StructuralAttributeTests {
        static void Check<T>(int size, string message = "") { Assert.AreEqual(StructuralAttribute.GetSize(typeof(T)), size, message); }

        class C1 {
            [Structural] public float a;
            [Structural] public float b;
            [Structural] public float c;

            public float d;
            public float e;
        }

        [Test] public void FindsMarkedPublicInstanceFields() => Check<C1>(3);

        class C2 {
            [Structural] float a;
            [Structural] float b;
            [Structural] float c;

            float d;
            float e;
        }

        [Test] public void FindsMarkedPrivateInstanceFields() => Check<C2>(3);


        class C3 {
            [Structural] public static float a;
            [Structural] public static float b;
            [Structural] public static float c;

            public static float d;
            public static float e;
        }

        [Test] public void FindsMarkedPublicStaticFields() => Check<C3>(3);

        class C4 {
            [Structural] static float a;
            [Structural] static float b;
            [Structural] static float c;

            static float d;
            static float e;
        }

        [Test] public void FindsMarkedPrivateStaticFields() => Check<C4>(3);

        class C5 {
            [Structural] Vector3 vector3;
            Vector3 vector3Hidden;
        }

        [Test] public void ReturnsThreeFromVector3() => Check<C5>(3);

        class C6 {
            [Structural] Vector2 vector2;
            Vector3 vector2Hidden;
        }

        [Test] public void ReturnsTwoFromVector2() => Check<C6>(2);

        class C7 {
            [Structural] float a;
            [Structural] Vector2 vector2;
            [Structural] Vector3 vector3;
        }

        [Test] public void ReturnsSumOfFloatVector2Vector3() => Check<C7>(1 + 2 + 3);

        class Base {
            [Structural] public float a;
            [Structural] protected float b;
            [Structural] float cPrivateSoMustBeHidden;

            public float aHidden;
            protected float bHidden;
            float cPrivateHidden;
        }

        class C8 : Base { }

        [Test] public void FindsInheritedMembers() => Check<C8>(2);
    }
}