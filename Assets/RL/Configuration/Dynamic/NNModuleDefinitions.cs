using System;
using System.Collections.Generic;
using System.Linq;
using JetBrains.Annotations;
using RL.Configuration.NN;
using RL.Exceptions;
using RL.NN;
using UnityEngine;

namespace RL.Configuration.Dynamic
{
    [CreateAssetMenu(fileName = "Layout", menuName = "NN Layout", order = 0)]
    public class NNModuleDefinitions : ScriptableObject
    {
        public List<Definition> definitions = new List<Definition>();
        public IEnumerable<string> DefinitionNames => definitions.Select(definition => definition.name);

        [CanBeNull] Definition this[string definitionName] => definitions.Find(definition => definition.name == definitionName);

        public IEnumerable<ModuleConfiguration> Compile(string definitionName, int inputSize = INFER, int outputSize = INFER)
        {
            // First, lets flatten the structure
            var modules = GetAllModules(definitionName).ToArray();

            var currentInput = inputSize;

            for (var i = 0; i < modules.Length; i++) {
                var (module, layerName) = modules[i];

                if (currentInput == INFER)
                    currentInput = GetInputSize(modules, i, outputSize);
                else if (!module.inputSizeInferred) throw new BaseException("Multiple input sizes provided");

                var currentOutput = !module.outputSizeInferred ? module.outputSizeFixed : GetOutputSize(modules, i, currentInput, outputSize);

                yield return new ModuleConfiguration(layerName,
                                                     new ModuleConfiguration.IntParametersDict {
                                                             {ModuleConfiguration.ModuleConfigurationParameterInt.InputSize, currentInput},
                                                             {ModuleConfiguration.ModuleConfigurationParameterInt.OutputSize, currentOutput},
                                                     },
                                                     new ModuleConfiguration.FloatParametersDict());

                currentInput = currentOutput;
            }
        }

        IEnumerable<(Module, ModuleLayerName)> GetAllModules(string definitionName)
        {
            var definition = this[definitionName];
            if (definition == null) throw new ConfigurationException($"Definition {definitionName} was not found");

            foreach (var module in definition.submodules)
                if (Enum.TryParse(module.definitionName, out ModuleLayerName layerName))
                    yield return (module, layerName);
                else
                    foreach (var m in GetAllModules(module.definitionName))
                        yield return m;
        }

        static int GetOutputSize((Module, ModuleLayerName name)[] modules, int moduleIndex, int inputSize, int outputSize)
        {
            var name = modules[moduleIndex].name;
            if (name == ModuleLayerName.ReLU || name == ModuleLayerName.Softmax)
                if (inputSize != INFER)
                    return inputSize;

            if (moduleIndex == modules.Length - 1) {
                if (outputSize == INFER) throw new BaseException("Output size missing");

                return outputSize;
            }

            return GetInputSize(modules, moduleIndex + 1, outputSize);
        }

        static int GetInputSize(IReadOnlyList<(Module module, ModuleLayerName name)> modules, int moduleIndex, int outputSize)
        {
            while (true) {
                var (module, name) = modules[moduleIndex];
                if (!module.inputSizeInferred) return module.inputSizeFixed;

                if (name == ModuleLayerName.ReLU || name == ModuleLayerName.Softmax) {
                    if (moduleIndex == modules.Count - 1) {
                        if (outputSize == INFER) throw new BaseException("Output size missing");

                        return outputSize;
                    }

                    moduleIndex += 1;
                    continue;
                }

                throw new BaseException("Input size missing for module " + moduleIndex);
            }
        }

        public const int INFER = -1;
    }
}
