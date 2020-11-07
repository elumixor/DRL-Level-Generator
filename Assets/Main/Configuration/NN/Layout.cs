using System;
using System.Collections.Generic;
using System.Linq;
using Common.ByteConversions;
using Configuration.Dynamic;
using JetBrains.Annotations;

namespace Configuration.NN
{
    [Serializable]
    public class Layout
    {
        public NNModuleDefinitions moduleDefinitions;
        public string selectedDefinition;

        public IEnumerable<ModuleConfiguration> Modules([ValueProvider("Configuration.Dynamic.NNModuleDefinitions")] int inputSize,
                                                        [ValueProvider("Configuration.Dynamic.NNModuleDefinitions")] int outputSize) =>
                moduleDefinitions.Compile(selectedDefinition, inputSize, outputSize);

        public IEnumerable<byte> ToBytes([ValueProvider("Configuration.Dynamic.NNModuleDefinitions")] int inputSize,
                                         [ValueProvider("Configuration.Dynamic.NNModuleDefinitions")] int outputSize)
        {
            var modules = Modules(inputSize, outputSize).ToArray();
            return modules.Length.ToBytes().Concat(modules.SelectMany(m => m.ToBytes()));
        }
    }
}
