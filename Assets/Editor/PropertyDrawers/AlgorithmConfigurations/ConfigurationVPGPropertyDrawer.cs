using RL.Configuration.AlgorithmConfigurations;
using UnityEditor;
using UnityEngine;

namespace Editor.PropertyDrawers.AlgorithmConfigurations
{
    [CustomPropertyDrawer(typeof(ConfigurationVPG))]
    public class ConfigurationVPGPropertyDrawer : PropertyDrawer
    {
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            EditorGUI.PropertyField(position, property.FindPropertyRelative("actor"));
        }

        /// <inheritdoc/>
        public override float GetPropertyHeight(SerializedProperty property, GUIContent label) => EditorGUIUtility.singleLineHeight;
    }
}
