import multiprocessing as mp
import time
from threading import Thread
from typing import Union, List

import zmq

from common import ByteReader
from remote_computation import model_manager
from remote_computation.message_type import MessageType
from serialization import to_bytes


def _process_message(message: bytes, result: List[bytes]):
    reader = ByteReader(message)

    request_id = reader.read_int()
    message_type = MessageType(reader.read_int())

    if message_type == MessageType.ObtainModel:
        model_id = reader.read_to_end()

        model = model_manager.obtain_new(model_id)

        result[:] = list(to_bytes(request_id) + model.response_bytes)
        return

    if message_type == MessageType.LoadModel:
        file_path = reader.read_string()

        model = model_manager.load_model(file_path)

        result[:] = list(to_bytes(request_id) + model.response_bytes)
        return

    if message_type == MessageType.SaveModel:
        model_id = reader.read_int()
        file_path = reader.read_string()

        model_manager.save_model(model_id, file_path)

        result[:] = list(to_bytes(request_id))
        return

    if message_type == MessageType.RunTask:
        model_id = reader.read_int()
        task = reader.read_to_end()

        model = model_manager.get(model_id)
        result = model.run_task(task)

        result[:] = list(to_bytes(request_id) + result)
        return

    raise RuntimeError(f"Unknown message type: {message_type}")


class Communicator:
    update_time = 0.05

    def __init__(self, pull_port: int, push_port: int):
        self.pull = zmq.Context().socket(zmq.PULL)
        self.pull.bind(f"tcp://*:{pull_port}")

        self.push = zmq.Context().socket(zmq.PUSH)
        self.push.connect(f"tcp://localhost:{push_port}")

        self.should_stop = False

        self.update_worker: Union[mp.Process, None] = None
        self.request_handlers: List[Thread] = []

        self.manager = mp.Manager()

    def start_update_loop(self):
        self.update_worker = Thread(target=self._update_loop)
        self.update_worker.start()

    def join(self):
        self.should_stop = True

        for handler in self.request_handlers:
            handler.join()

        self.update_worker.join()

    def _update_loop(self):
        while not self.should_stop:
            try:
                message = self.pull.recv(flags=zmq.NOBLOCK)
                self.request_handlers.append(Thread(target=self._process_message(message)))

            except zmq.Again as _:
                pass

            time.sleep(Communicator.update_time)

    def _process_message(self, message: bytes):
        print(f"Message received ({len(message)}B)")

        result = self.manager.list()
        handler = mp.Process(target=_process_message, args=(message, result))
        handler.start()
        handler.join()

        self.push.send(b''.join(result))
