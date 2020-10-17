using System;
using System.Reflection;
using UnityEngine;

namespace Serialization {
    /// <summary>
    /// We are using this attribute to mark members of our state and action that will be used in training,
    /// so that we know the size of data which we are sending and receiving from backend 
    /// </summary>
    [AttributeUsage(AttributeTargets.Field | AttributeTargets.Property)]
    public class StructuralAttribute : Attribute {
        const BindingFlags BINDINGS = BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic;

        /// <summary>
        /// Returns the total number of floats in a type. Searches for <see cref="Vector3"/>, <see cref="Vector2"/> and float members,
        /// marked with the [Structural] attribute
        /// </summary>
        /// <param name="target">Type to be examined</param>
        /// <returns>Total number of floats</returns>
        public static int GetSize(Type target) {
            var sum = 0;
            foreach (var member in target.GetMembers(BINDINGS)) {
                if (!member.IsDefined(typeof(StructuralAttribute))) continue;

                switch (member) {
                    case FieldInfo fieldInfo: {
                        var type = fieldInfo.FieldType;

                        if (type == typeof(float))
                            sum += 1;
                        else if (type == typeof(Vector2))
                            sum += 2;
                        else if (type == typeof(Vector3))
                            sum += 3;
                        break;
                    }
                    case PropertyInfo propertyInfo when !propertyInfo.CanRead:
                        throw new Exception("StructuralAttribute is only valid on properties that can be read.");
                    case PropertyInfo propertyInfo: {
                        var type = propertyInfo.PropertyType;

                        if (type == typeof(float))
                            sum += 1;
                        else if (type == typeof(Vector2))
                            sum += 2;
                        else if (type == typeof(Vector3))
                            sum += 3;
                        break;
                    }
                }
            }

            return sum;
        }
    }
}