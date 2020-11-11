using RL.RLBehaviours;
using UnityEditor;
using UnityEngine;

namespace Editor.PropertyDrawers
{
    [CustomPropertyDrawer(typeof(InstanceSpawner))]
    public class InstanceSpawnerPropertyDrawer : PropertyDrawer
    {
        bool isOpen;
        readonly int boxPadding = 2;

        /// <inheritdoc/>
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            GUI.Box(position, GUIContent.none);

            position.x      += boxPadding;
            position.y      += boxPadding;
            position.width  -= boxPadding * 2;
            position.height -= boxPadding * 2;

            var spacing = EditorGUIUtility.standardVerticalSpacing;
            var labelWidth = EditorGUIUtility.labelWidth;
            var lineHeight = EditorGUIUtility.singleLineHeight;

            var propertyX = position.x                     + labelWidth + spacing;
            var propertyWidth = position.width - propertyX + position.x;

            const int countFieldWidth = 50;
            const int totalShapeWidth = 100;

            var countProperty = property.FindPropertyRelative("count");
            var rowsProperty = property.FindPropertyRelative("rows");
            var columnSpacingProperty = property.FindPropertyRelative("columnSpacing");
            var rowSpacingProperty = property.FindPropertyRelative("rowSpacing");

            // Object field, Count
            EditorGUI.BeginProperty(position, label, property);
            var isOpenChanged = GUI.Button(new Rect(position.x, position.y, labelWidth, lineHeight), label, EditorStyles.foldout);
            if (isOpenChanged) isOpen = !isOpen;

            var r = new Rect(propertyX, position.y, propertyWidth - countFieldWidth - spacing, lineHeight);
            EditorGUI.ObjectField(r, property.FindPropertyRelative("environment"), typeof(MonoBehaviour), GUIContent.none);

            r.x     += r.width + spacing;
            r.width =  countFieldWidth;

            var guiStyle = EditorStyles.numberField;
            guiStyle.alignment     = TextAnchor.MiddleRight;
            countProperty.intValue = EditorGUI.IntField(r, countProperty.intValue, guiStyle);
            EditorGUI.EndProperty();

            // Advanced parameters dropdown
            if (!isOpen) return;

            r                     = new Rect(position.x, position.y + lineHeight + spacing, position.width - totalShapeWidth - spacing, lineHeight);
            rowsProperty.intValue = EditorGUI.IntField(r, "Rows", rowsProperty.intValue);

            r.x     += r.width + spacing;
            r.width =  totalShapeWidth;
            var columns = Mathf.CeilToInt((float) property.FindPropertyRelative("count").intValue / rowsProperty.intValue);
            EditorGUI.LabelField(r, $"[{columns} x {rowsProperty.intValue}]", new GUIStyle {alignment = TextAnchor.MiddleRight});

            r.x     =  position.x;
            r.width =  position.width;
            r.y     += lineHeight + spacing;

            columnSpacingProperty.floatValue = EditorGUI.FloatField(r, "Column spacing", columnSpacingProperty.floatValue);

            r.y += lineHeight + spacing;

            rowSpacingProperty.floatValue = EditorGUI.FloatField(r, "Row spacing", rowSpacingProperty.floatValue);

            //    rows (max number of items in row)

            // Bonus: warning/error when the object does not contain RLBehaviours.EnvironmentInstance
            //        and grey-out the rest of gui
        }

        /// <inheritdoc/>
        public override float GetPropertyHeight(SerializedProperty property, GUIContent label) =>
                EditorGUIUtility.singleLineHeight * (isOpen ? 4 : 1) + (isOpen ? EditorGUIUtility.standardVerticalSpacing * 3 : 0) + boxPadding * 2;
    }
}
