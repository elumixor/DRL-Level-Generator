using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using NUnit.Framework;
using Serialization;
using UnityEngine;

namespace Testing.EditorTests {
    public class ReflectionTests {

        abstract class Base {
            [Structural] float shouldNotBeInherited = 5;
            [Structural] protected float shouldBeInherited = 6;
            [Structural] protected abstract float inheritedMethod();
        }

        class C1 : Base {
            float privateField = 5;
            public float publicField = 5;
            static float staticField = 5;
            public float Method() => 5;
            static float Getter => 5;

            [Structural] float markedPrivateField = 1;
            [Structural] public float markedPublicField = 2;
            [Structural] static float markedStaticField = 3;
            [Structural] public float markedMethod() => 4;
            [Structural] static float markedGetter => 5;

            protected override float inheritedMethod() { return 7; }
        }

        static IEnumerable<MemberInfo> GetMembers(Type t) =>
            t.GetMembers(BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic)
                .Where(member => member.IsDefined(typeof(StructuralAttribute), true));

        // A Test behaves as an ordinary method
        [Test]
        public void FindingMembersByCustomAttributePasses() {
            // Use the Assert class to test conditions

            var properties = GetMembers(typeof(C1)).ToArray();
            Assert.AreEqual(7, properties.Length, "Should return exactly seven marked properties");
        }

        class C2 {
            [Structural] float field = 1;
            [Structural] string wrongField = "wrong";
            [Structural] float Getter => 2;
            [Structural] string WrongGetter => "wrong";
            [Structural] float Method() => 3;
            [Structural] string WrongMethod() => "wrong";
            [Structural] Vector3 MethodVector3() => Vector3.one * 4;
            [Structural] Vector2 MethodVector2() => Vector2.one * 5;
        }

        static bool CheckCorrectType(Type t) => t == typeof(float) || t == typeof(Vector3) || t == typeof(Vector2);

        static IEnumerable<Type> GetMembersWithCorrectType(Type t) =>
            GetMembers(typeof(C2)).Select(member => {
                switch (member) {
                    case FieldInfo fieldInfo:
                        return fieldInfo.FieldType;
                    case PropertyInfo propertyInfo:
                        return propertyInfo.PropertyType;
                    case MethodInfo memberInfo:
                        return memberInfo.ReturnType;
                    default:
                        throw new Exception("Member is not a field, property or a method?");
                }
            }).Where(CheckCorrectType);

        // A Test behaves as an ordinary method
        [Test]
        public void FindingMembersThatHaveFloatOrVec3ReturnTypePasses() {
            // Use the Assert class to test conditions

            var properties = GetMembersWithCorrectType(typeof(C2)).ToArray();
            Assert.AreEqual(5, properties.Length, "Should return exactly 4 marked properties with the correct type");
        }


        [Test]
        public void ShouldCalculateTheCorrectSizeOfAClass() {
            var length = GetMembersWithCorrectType(typeof(C2)).Select(GetFieldSize).Sum();
            Assert.AreEqual(length, 3 + 2 + 3, "Should return 8 floats");
        }

        static int GetFieldSize(Type t) { return t == typeof(Vector3) ? 3 : t == typeof(Vector2) ? 2 : 1; }
    }
}