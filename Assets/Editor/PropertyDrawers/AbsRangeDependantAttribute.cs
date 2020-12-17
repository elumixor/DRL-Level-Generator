using UnityEngine;

namespace Editor.PropertyDrawers
{
    public class AbsRangeDependantAttribute : PropertyAttribute
    {
        public readonly string dependantPropertyName;
        public AbsRangeDependantAttribute(string dependantPropertyName) => this.dependantPropertyName = dependantPropertyName;
    }
}
