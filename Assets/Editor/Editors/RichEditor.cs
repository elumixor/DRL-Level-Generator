using UnityEditor;

namespace Editor.Editors
{
    public class RichEditor : UnityEditor.Editor
    {
        protected float Spacing => EditorGUIUtility.standardVerticalSpacing;
        protected float LineHeight => EditorGUIUtility.singleLineHeight;
    }
}
