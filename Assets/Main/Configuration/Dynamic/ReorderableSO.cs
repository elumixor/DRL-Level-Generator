using System.Collections.Generic;
using UnityEditor;
using UnityEditorInternal;
using UnityEngine;

namespace Configuration.Dynamic
{
    [CreateAssetMenu(fileName = "Reorderable", menuName = "Reorderable", order = 0)]
    public class ReorderableSO : ScriptableObject
    {
        public List<string> items;

        [CustomEditor(typeof(ReorderableSO))]
        public class ReorderableEditor : UnityEditor.Editor
        {
            ReorderableSO reorderable;
            ReorderableList list;

            void OnEnable()
            {
                reorderable = (ReorderableSO) target;
                list = new ReorderableList(serializedObject, serializedObject.FindProperty("items")) {
                        drawElementCallback = (rect, i, active, focused) => { reorderable.items[i] = EditorGUI.TextField(rect, reorderable.items[i]); },
                };
                list.elementHeightCallback = i => (EditorGUIUtility.standardVerticalSpacing + EditorGUIUtility.singleLineHeight) * (i + 1);
            }

            /// <inheritdoc/>
            public override void OnInspectorGUI()
            {
                serializedObject.Update();
                list.DoLayoutList();
                serializedObject.ApplyModifiedProperties();
            }
        }
    }
}
