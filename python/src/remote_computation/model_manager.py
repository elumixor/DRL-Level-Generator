from typing import Dict

from common import ByteReader
from .models import RemoteModel, DQNModel, ModelType

MD = Dict[int, RemoteModel]
model_dict: MD = dict()


def _next_model_id():
    i = 0
    while i in model_dict:
        i += 1
    return i


def get(model_id) -> RemoteModel:
    return model_dict[model_id]


def obtain_new(reader: ByteReader) -> RemoteModel:
    model_type = ModelType(reader.read_int())

    if model_type == ModelType.DQN:
        model_id = _next_model_id()
        model = DQNModel(model_id, reader)
        model_dict[model_id] = model
        return model

    raise RuntimeError(f"Unknown model type: {model_type}")


def load_model(file_path) -> RemoteModel:
    f = open(file_path, 'rb')
    reader = ByteReader(f.read())
    f.close()
    model_type = ModelType(reader.read_int())

    if model_type == ModelType.DQN:
        model_id = _next_model_id()
        model = DQNModel(model_id, reader)
        model.load_from_file(reader)
        model_dict[model_id] = model
        return model

    raise RuntimeError(f"Unknown model type: {model_type}")


def save_model(model_id: int, file_path: str):
    model = get(model_id)

    f = open(file_path, 'wb')
    f.write(model.save_bytes)
    f.close()
