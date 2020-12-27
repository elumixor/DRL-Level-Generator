import multiprocessing as mp
import time
from concurrent.futures._base import Future
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread
from typing import Union, List

import zmq

import remote_computation.model_manager as model_manager
from common import ByteReader
from serialization import to_bytes
from . import logging
from .logging import LogOptions
from .message_type import MessageType


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
        self.request_handlers: List[Future[None]] = []

        self.executor = ThreadPoolExecutor()

    def start_update_loop(self):
        self.update_worker = Thread(target=self._update_loop)
        self.update_worker.start()

    def join(self):
        for handler in self.request_handlers:
            handler.result()

        self.update_worker.join()
        self.is_running = False

    def _update_loop(self):
        self.is_running = True
        while not self.should_stop:
            try:
                message = self.pull.recv(flags=zmq.NOBLOCK)
                thread = self.executor.submit(self._process_message, message)
                self.request_handlers.append(thread)

            except zmq.Again as _:
                pass

            time.sleep(Communicator.update_time)

    def _process_message(self, message: bytes):
        print(f"Message received ({len(message)}B)")

        reader = ByteReader(message)

        request_id = reader.read_int()
        message_type = MessageType(reader.read_int())

        def OK(b: bytes = b''):
            """Helper to return the response with given data"""
            print(f"sending ({len(b)}B)")
            self.push.send(to_bytes(request_id) + b)

        # Handlers of various message types

        if message_type == MessageType.RunTask:
            model_id = reader.read_int()
            model = model_manager.get(model_id)
            task_result = model.run_task(reader)
            return OK(task_result)

        if message_type == MessageType.ObtainModel:
            model = model_manager.obtain_new(reader)
            return OK(model.response_bytes)

        if message_type == MessageType.LoadModel:
            file_path = reader.read_string()
            model = model_manager.load_model(file_path)
            return OK(model.response_bytes)

        if message_type == MessageType.SaveModel:
            model_id = reader.read_int()
            file_path = reader.read_string()
            model_manager.save_model(model_id, file_path)
            return OK()

        if message_type == MessageType.SetLogOptions:
            model_id = reader.read_int()
            model = model_manager.get(model_id)
            log_options = LogOptions(reader)
            logging.register(model.model_id, log_options)
            return OK()

        if message_type == MessageType.ShowLog:
            model_id = reader.read_int()
            model = model_manager.get(model_id)
            logging.show(model.model_id, model.log_data)
            return OK()

        # Test message

        if message_type == MessageType.Test:
            print("Test")
            data = reader.read_to_end()
            print(f"Received: {data}")
            return OK(data)

        # Unknown message type - throw error

        raise RuntimeError(f"Unknown message type: {message_type}")
