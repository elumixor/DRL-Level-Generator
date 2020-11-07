using System;
using System.Linq;
using Configuration.Dynamic;
using Configuration.NN;
using UnityEditor;
using UnityEngine;

namespace Editor.PropertyDrawers
{
    [CustomPropertyDrawer(typeof(Layout))]
    public class LayoutPropertyDrawer : PropertyDrawer
    {
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            // Module definitions and dynamic popup to select the top-level definition
            position = EditorGUI.PrefixLabel(position, label);

            var moduleDefinitionsProperty = property.FindPropertyRelative("moduleDefinitions");
            var moduleDefinitions = (NNModuleDefinitions) moduleDefinitionsProperty.objectReferenceValue;

            if (moduleDefinitions == null) {
                EditorGUI.ObjectField(position, moduleDefinitionsProperty, GUIContent.none);
                return;
            }

            position.width -= EditorGUIUtility.standardVerticalSpacing;
            position.width /= 2;

            EditorGUI.ObjectField(position, moduleDefinitionsProperty, GUIContent.none);
            position.x += position.width + EditorGUIUtility.standardVerticalSpacing;

            var definitionNames = moduleDefinitions.DefinitionNames.ToArray();

            if (definitionNames.Length < 1) {
                EditorGUI.LabelField(position, "No Definitions", new GUIStyle(EditorStyles.label) {alignment = TextAnchor.MiddleCenter});
                return;
            }

            var selectedDefinitionProperty = property.FindPropertyRelative("selectedDefinition");
            var selectedDefinition = selectedDefinitionProperty.stringValue;
            var currentIndex = Array.IndexOf(definitionNames, selectedDefinition);

            if (currentIndex < 0) selectedDefinitionProperty.stringValue = definitionNames[currentIndex = 0];

            currentIndex = EditorGUI.Popup(position, currentIndex, definitionNames);

            selectedDefinitionProperty.stringValue = definitionNames[currentIndex];
        }
    }
}
