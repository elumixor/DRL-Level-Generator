import threading
from typing import Callable, Union

import zmq

import serialization
from serialization import Endianness
from utilities import log
from .request_type import RequestType
from .response_type import ResponseType
from .server_exception import ServerException


# print(f"Current libzmq version is {zmq.zmq_version()}")
# print(f"Current  pyzmq version is {zmq.__version__}")


class Server:
    def __init__(self, address: str, handle_message: Callable[[RequestType, bytes], None]):
        self.__context: zmq.Context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REP)
        self.__address = address
        self.__handle_message = handle_message
        self.__is_running = False
        self.__thread: Union[threading.Thread, None] = None

    @property
    def is_running(self):
        return self.__is_running

    def start(self):
        if self.__is_running:
            raise ServerException("Server is already running")

        self.__is_running = True

        def thread_function(server: Server):
            server.__socket.bind(self.__address)
            log("Server started")
            while self.__is_running:
                try:
                    request_bytes = self.__socket.recv(zmq.DONTWAIT)
                    request_type, start_index = serialization.to_string(request_bytes, 0, Endianness.Little)
                    data = request_bytes[start_index:]

                    try:
                        request_type = RequestType[request_type]
                    except KeyError:
                        raise ServerException(f"Invalid request type: {request_type}")

                    log(f"Request received: [{request_type}] {len(data)} bytes")
                    server.__handle_message(RequestType[request_type], data)
                except zmq.Again:
                    pass
                except Exception as e:
                    server.send_message(ResponseType.Failure, serialization.to_bytes(str(e)))
                    raise e
            log("Server stopped")

        self.__thread = threading.Thread(target=thread_function, args=(self,), daemon=True)
        self.__thread.start()

    def stop(self):
        if not self.__is_running:
            return

        log("Server stopping...")
        self.__is_running = False

    def send_message(self, response_type: ResponseType, data: bytes = b''):
        self.__socket.send(serialization.to_bytes(response_type) + data)

    def wait_for_stop(self):
        if self.__thread is not None:
            self.__thread.join()
