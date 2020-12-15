import multiprocessing as mp
import time
from threading import Thread
from typing import Union, List

import zmq

from common import ByteReader
from remote_computation import model_manager
from remote_computation.message_type import MessageType
from serialization import to_bytes


def _process_message(message: bytes, models_dict, result: List[bytes]):
    reader = ByteReader(message)

    request_id = reader.read_int()
    message_type = MessageType(reader.read_int())

    if message_type == MessageType.ObtainModel:
        model = model_manager.obtain_new(models_dict, reader)

        result[:] = list(to_bytes(request_id) + model.response_bytes)
        return

    if message_type == MessageType.LoadModel:
        file_path = reader.read_string()

        model = model_manager.load_model(models_dict, file_path)

        result[:] = list(to_bytes(request_id) + model.response_bytes)
        return

    if message_type == MessageType.SaveModel:
        model_id = reader.read_int()
        file_path = reader.read_string()

        model_manager.save_model(models_dict, model_id, file_path)

        result[:] = list(to_bytes(request_id))
        return

    if message_type == MessageType.RunTask:
        model_id = reader.read_int()

        model = model_manager.get(models_dict, model_id)
        task_result = model.run_task(reader)

        result[:] = list(to_bytes(request_id) + task_result)
        return

    if message_type == MessageType.Test:
        print(f"Received: {reader.read_int()}")
        print(request_id)
        print(to_bytes(request_id))
        print(list(to_bytes(request_id)))
        result[:] = list(to_bytes(request_id))
        print(result)
        return

    raise RuntimeError(f"Unknown message type: {message_type}")


class Communicator:
    update_time = 0.05

    PULL_PORT = 5671
    PUSH_PORT = 5672

    def __init__(self):
        self.pull = zmq.Context().socket(zmq.PULL)
        self.pull.bind(f"tcp://*:{Communicator.PULL_PORT}")

        self.push = zmq.Context().socket(zmq.PUSH)
        self.push.connect(f"tcp://localhost:{Communicator.PUSH_PORT}")

        self.should_stop = False
        self.is_running = False

        self.update_worker: Union[mp.Process, None] = None
        self.request_handlers: List[Thread] = []

        self.manager = mp.Manager()
        self.models_dict = self.manager.dict()

    def start_update_loop(self):
        self.update_worker = Thread(target=self._update_loop)
        self.update_worker.start()

    def join(self):
        self.should_stop = True

        for handler in self.request_handlers:
            handler.join()

        self.update_worker.join()
        self.is_running = False

    def _update_loop(self):
        self.is_running = True
        while not self.should_stop:
            try:
                message = self.pull.recv(flags=zmq.NOBLOCK)
                thread = Thread(target=self._process_message(message))
                self.request_handlers.append(thread)
                thread.start()

            except zmq.Again as _:
                pass

            time.sleep(Communicator.update_time)

    def _process_message(self, message: bytes):
        print(f"Message received ({len(message)}B)")

        result = self.manager.list()
        handler = mp.Process(target=_process_message, args=(message, self.models_dict, result))
        handler.start()
        handler.join()

        self.push.send(bytes(result))
