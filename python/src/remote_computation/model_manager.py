from typing import Dict

from common import ByteReader
from .models import RemoteModel, DQNModel, ModelType

current_model_id = 0

models: Dict[int, RemoteModel] = dict()


def _next_model_id():
    global current_model_id
    result = current_model_id
    current_model_id += 1
    return result


def get(model_id) -> RemoteModel:
    return models[model_id]


def obtain_new(reader: ByteReader) -> RemoteModel:
    model_type = ModelType(reader.read_int())

    if model_type == ModelType.DQN:
        model = DQNModel(_next_model_id(), reader)
        return model

    raise RuntimeError(f"Unknown model type: {model_type}")


def load_model(file_path) -> RemoteModel:
    f = open(file_path, 'rb')
    reader = ByteReader(f.read())
    f.close()
    model_type = ModelType(reader.read_int())

    if model_type == ModelType.DQN:
        model = DQNModel(_next_model_id())
        model.load_from_file(reader)
        return model

    raise RuntimeError(f"Unknown model type: {model_type}")


def save_model(model_id: int, file_path: str):
    model = get(model_id)

    f = open(file_path, 'wb')
    f.write(model.save_bytes)
    f.close()
