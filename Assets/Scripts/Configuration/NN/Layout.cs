using System;
using System.Collections.Generic;

namespace Configuration.NN {
    [Serializable]
    public partial class Layout {
        bool displayed;
        public List<ModuleConfiguration> modules = new List<ModuleConfiguration>();
    }
}