﻿using System;
using Configuration.NN;
using Exceptions;
using NN;

namespace Serialization
{
    public static class NNSerializer
    {
        public static Module ToModule(this ModuleConfiguration moduleConfiguration)
        {
            var (layerName, _, intParameters) = moduleConfiguration;
            switch (layerName) {
                case ModuleLayerName.Linear:
                    return new Linear(intParameters[ModuleConfiguration.ModuleConfigurationParameterInt.InputSize],
                                      intParameters[ModuleConfiguration.ModuleConfigurationParameterInt.OutputSize]);
                case ModuleLayerName.ReLU:       return new ReLU();
                case ModuleLayerName.Softmax:    return new Softmax();
                case ModuleLayerName.Sequential: throw new BaseException("Nested sequential layers are not supported yet");
                case ModuleLayerName.Identity:   return new Identity();
                default:                         throw new ArgumentOutOfRangeException();
            }
        }
    }
}
