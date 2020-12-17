using UnityEditor;
using UnityEngine;

namespace Editor.PropertyDrawers
{
    [CustomPropertyDrawer(typeof(PlusMinusAttribute))]
    public class PlusMinusPropertyDrawer : PropertyDrawer
    {
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            var plusMinus = (PlusMinusAttribute) attribute;

            position = EditorGUI.PrefixLabel(position, label);
            var value = property.floatValue;

            if (GUI.Button(position, value > 0 ? plusMinus.PositiveLabel : plusMinus.NegativeLabel)) value = value > 0 ? -1f : 1f;

            if (Mathf.Abs(value - 1f) > 1e-5f && Mathf.Abs(value + 1f) > 1e-5f) value = 1f;
            property.floatValue = value;
        }
    }
}
