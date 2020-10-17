using System;
using System.Linq;
using System.Reflection;
using UnityEngine;

namespace Serialization {
    /// <summary>
    /// We are using this attribute to mark members of our state and action that will be used in training,
    /// so that we know the size of data which we are sending and receiving from backend 
    /// </summary>
    [AttributeUsage(AttributeTargets.Field | AttributeTargets.Property | AttributeTargets.Method)]
    public class StructuralAttribute : Attribute {
        // Filters correct member types
        static Type GetMembersTypes(MemberInfo member) {
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
        }

        // Maps members to sizes
        static int GetFieldSize(Type t) { return t == typeof(Vector3) ? 3 : t == typeof(Vector2) ? 2 : t == typeof(float) ? 1 : 0; }

        /// <summary>
        /// Returns the total number of floats in a type. Searches for <see cref="Vector3"/>, <see cref="Vector2"/> and float members,
        /// marked with the [Structural] attribute
        /// </summary>
        /// <param name="target">Type to be examined</param>
        /// <returns>Total number of floats</returns>
        public static int GetSize(Type target) {
            var members = target.GetMembers(BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
            var marked = members.Where(member => member.IsDefined(typeof(StructuralAttribute), true));
            var memberTypes = marked.Select(GetMembersTypes);
            var totalSize = memberTypes.Select(GetFieldSize).Sum();
            return totalSize;
        }
    }
}