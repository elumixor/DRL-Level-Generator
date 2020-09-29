import time
import zmq
from utilities import Event

context = zmq.Context()
socket = context.socket(zmq.REP)
address = "tcp://*:5555"
socket.bind(address)

on_message = Event()


def start_server():
    print(f"Server started on {address}")
    while True:
        # Wrap in a try catch block to prevent Unity freezing on an error
        try:
            on_message(socket.recv())
        except Exception as e:
            send_message(bytes("Error on backend", "ascii"), True)
            raise e


def send_message(message, is_error=False):
    socket.send((b'e' if is_error else b'o') + message)
