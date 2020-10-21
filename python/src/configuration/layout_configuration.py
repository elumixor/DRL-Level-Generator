import serialization
from .nn import *


def bytes_to_int_parameter(data: bytes, start: int, _):
    parameter_name_str, total_read = serialization.to_string(data, start)
    parameter_name = IntParameter(parameter_name_str)

    parameter_value = serialization.to_int(data, start + total_read)
    total_read += serialization.DataTypesSize.Int

    return (parameter_name, parameter_value), total_read


def bytes_to_float_parameter(data: bytes, start: int, _):
    parameter_name_str, total_read = serialization.to_string(data, start)
    parameter_name = FloatParameter(parameter_name_str)

    parameter_value = serialization.to_float(data, start + total_read)
    total_read += serialization.DataTypesSize.Float

    return (parameter_name, parameter_value), total_read


def bytes_to_layer(data: bytes, start: int, _):
    layer_name_str, total_read = serialization.to_string(data, start)
    layer_name = LayerName(layer_name_str)

    int_parameters, bytes_read = serialization.to_list(data, bytes_to_int_parameter, start + total_read)
    int_parameters = {name: value for (name, value) in int_parameters}
    total_read += bytes_read

    float_parameters, bytes_read = serialization.to_list(data, bytes_to_float_parameter, start + total_read)
    float_parameters = {name: value for (name, value) in float_parameters}
    total_read += bytes_read

    return (layer_name, int_parameters, float_parameters), total_read


class LayoutConfiguration:
    def __init__(self, bytes_data: bytes, start_index: int):
        self.modules, self.bytes_read = serialization.to_list(bytes_data, bytes_to_layer, start_index)
