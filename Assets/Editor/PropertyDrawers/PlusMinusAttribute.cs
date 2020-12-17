using UnityEngine;

namespace Editor.PropertyDrawers
{
    public class PlusMinusAttribute : PropertyAttribute
    {
        public string PositiveLabel { get; set; } = "Positive";
        public string NegativeLabel { get; set; } = "Negative";
    }
}
