using System.Collections.Generic;
using UnityEngine;

namespace Configuration.Dynamic
{
    [CreateAssetMenu(fileName = "DynamicLayout", menuName = "Dynamic Layout", order = 0)]
    public class LayoutSO : ScriptableObject
    {
        public List<Definition> definitions = new List<Definition>();
    }
}
