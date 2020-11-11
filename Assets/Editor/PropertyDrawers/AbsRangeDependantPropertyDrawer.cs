using UnityEditor;
using UnityEngine;

namespace Editor.PropertyDrawers
{
    [CustomPropertyDrawer(typeof(AbsRangeDependantAttribute))]
    public class AbsRangeDependantPropertyDrawer : PropertyDrawer
    {
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            var attr = (AbsRangeDependantAttribute) attribute;
            var dependantValue = property.serializedObject.FindProperty(attr.dependantPropertyName).floatValue;
            EditorGUI.Slider(position, property, -dependantValue, dependantValue, label);
        }
    }
}
