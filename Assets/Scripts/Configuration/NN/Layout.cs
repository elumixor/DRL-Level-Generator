using System;
using System.Collections.Generic;
using Common.ByteConversions;

namespace Configuration.NN {
    [Serializable]
    public partial class Layout {
        bool displayed;
        public List<ModuleConfiguration> modules = new List<ModuleConfiguration>();

        public IEnumerable<byte> ToBytes() => modules.ToBytes(modules.Count);
    }
}