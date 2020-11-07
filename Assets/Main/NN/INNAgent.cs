﻿using System.Collections.Generic;
using Configuration.NN;

namespace NN
{
    /// <summary> Agent with NN </summary>
    public interface INNAgent
    {
        void ConstructNN(IEnumerable<ModuleConfiguration> modules);
        void SetParameters(StateDict stateDict);
    }
}
