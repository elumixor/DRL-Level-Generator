using System;
using System.Collections.Generic;
using Common;

namespace Configuration.NN {
    [Serializable]
    public class IntParametersDict : SerializableDictionary<ModuleConfigurationParameterInt, int> { }
}