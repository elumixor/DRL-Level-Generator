using System;
using System.Collections.Generic;
using System.Linq;
using JetBrains.Annotations;
using RL.Common.ByteConversions;
using RL.Configuration.Dynamic;

namespace RL.Configuration.NN
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
