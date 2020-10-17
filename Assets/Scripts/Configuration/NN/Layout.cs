using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using NN;
using UnityEditor;
using UnityEngine;

namespace Configuration.NN {
    [Serializable]
    public partial class Layout {
        public List<ModuleConfiguration> modules = new List<ModuleConfiguration>();
        bool displayed;
    }
}