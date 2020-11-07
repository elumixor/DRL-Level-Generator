using System;
using Configuration;
using UnityEditor;

namespace Editor.Editors
{
    [CustomEditor(typeof(TrainingConfiguration))]
    public class TrainingConfigurationEditor : UnityEditor.Editor
    {
        public override void OnInspectorGUI()
        {
            serializedObject.Update();

            EditorGUILayout.PropertyField(serializedObject.FindProperty("actionSize"));

            var algorithmProperty = serializedObject.FindProperty("algorithm");
            EditorGUILayout.PropertyField(algorithmProperty);

            var algorithm = (Algorithm) algorithmProperty.enumValueIndex;

            switch (algorithm) {
                case Algorithm.VPG:
                    EditorGUILayout.PropertyField(serializedObject.FindProperty("configurationVPG"));
                    break;
                case Algorithm.A2C:
                    EditorGUILayout.PropertyField(serializedObject.FindProperty("configurationA2C"));
                    break;
                default: throw new ArgumentOutOfRangeException();
            }

            serializedObject.ApplyModifiedProperties();
            EditorUtility.SetDirty(target);
        }
    }
}
