using TrainingSetups.Pendulum.Scripts;
using UnityEditor;
using UnityEngine;

namespace TrainingSetups.Pendulum.Editor
{
    [CustomPropertyDrawer(typeof(EnvironmentParameter))]
    public class EnvironmentParameterPropertyDrawer : PropertyDrawer
    {
        const float BUTTON_WIDTH = 75f;

        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            position = EditorGUI.PrefixLabel(position, label);

            var isConstantProperty = property.FindPropertyRelative("isConstant");
            var isConstant = isConstantProperty.boolValue;

            if (isConstant) {
                if (GUI.Button(new Rect(position) {width = BUTTON_WIDTH}, "Constant")) isConstantProperty.boolValue = false;

                position.x     += BUTTON_WIDTH + EditorGUIUtility.standardVerticalSpacing;
                position.width -= BUTTON_WIDTH - EditorGUIUtility.standardVerticalSpacing;

                EditorGUI.PropertyField(position, property.FindPropertyRelative("constantValue"), GUIContent.none);
            } else {
                if (GUI.Button(new Rect(position) {width = BUTTON_WIDTH}, "Variable")) isConstantProperty.boolValue = true;

                position.x     += BUTTON_WIDTH + EditorGUIUtility.standardVerticalSpacing;
                position.width -= BUTTON_WIDTH - EditorGUIUtility.standardVerticalSpacing;

                position.width = (position.width - EditorGUIUtility.standardVerticalSpacing) / 2;

                EditorGUI.PropertyField(position, property.FindPropertyRelative("rangeMin"), GUIContent.none);

                position.x += position.width + EditorGUIUtility.standardVerticalSpacing;

                EditorGUI.PropertyField(position, property.FindPropertyRelative("rangeMax"), GUIContent.none);
            }
        }

        /// <inheritdoc/>
        public override float GetPropertyHeight(SerializedProperty property, GUIContent label) => EditorGUIUtility.singleLineHeight;
    }
}
