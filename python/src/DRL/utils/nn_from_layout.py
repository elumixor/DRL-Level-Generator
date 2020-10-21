import torch

from configuration.configuration_exception import ConfigurationException
from configuration.layout_configuration import LayoutConfiguration, LayerName, IntParameter


def create_module(module_configuration) -> torch.nn.Module:
    module_name, int_parameters, float_parameters = module_configuration

    if module_name == LayerName.Linear:
        return torch.nn.Linear(int_parameters[IntParameter.InputSize], int_parameters[IntParameter.OutputSize])

    if module_name == LayerName.ReLU:
        return torch.nn.ReLU()

    if module_name == LayerName.Softmax:
        return torch.nn.Softmax()

    raise ConfigurationException(f"Unsupported layer name: {module_name}")


def nn_from_layout(layout: LayoutConfiguration) -> torch.nn.Module:
    return torch.nn.Sequential(*[create_module(module) for module in layout.modules])
