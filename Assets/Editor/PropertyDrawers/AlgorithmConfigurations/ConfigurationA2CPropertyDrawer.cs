using RL.Configuration.AlgorithmConfigurations;
using UnityEditor;
using UnityEngine;

namespace Editor.PropertyDrawers
{
    [CustomPropertyDrawer(typeof(ConfigurationA2C))]
    public class ConfigurationA2CPropertyDrawer : PropertyDrawer
    {
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            var lineHeight = EditorGUIUtility.singleLineHeight;
            var spacing = EditorGUIUtility.standardVerticalSpacing;

            position.height = lineHeight;

            var networksTypeProperty = property.FindPropertyRelative("networksType");
            EditorGUI.PropertyField(position, networksTypeProperty);

            var networkType = (ConfigurationA2C.A2CNetworksType) networksTypeProperty.enumValueIndex;

            position.y += lineHeight + spacing;

            if (networkType == ConfigurationA2C.A2CNetworksType.Separate) {
                EditorGUI.PropertyField(position, property.FindPropertyRelative("actor"));
                position.y += lineHeight + spacing;

                EditorGUI.PropertyField(position, property.FindPropertyRelative("critic"));
            } else {
                EditorGUI.PropertyField(position, property.FindPropertyRelative("base"));
                position.y += lineHeight + spacing;

                EditorGUI.PropertyField(position, property.FindPropertyRelative("actorHead"));
                position.y += lineHeight + spacing;

                EditorGUI.PropertyField(position, property.FindPropertyRelative("criticHead"));
            }
        }

        /// <inheritdoc/>
        public override float GetPropertyHeight(SerializedProperty property, GUIContent label)
        {
            var numLines = 1 + ((ConfigurationA2C.A2CNetworksType) property.FindPropertyRelative("networksType").enumValueIndex
                             == ConfigurationA2C.A2CNetworksType.Separate
                                        ? 2
                                        : 3);
            return numLines * EditorGUIUtility.singleLineHeight + (numLines - 1) * EditorGUIUtility.standardVerticalSpacing;
        }
    }
}
