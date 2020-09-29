import time
import zmq
from utilities import Event

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

on_message = Event()


def start_server():
    while True:
        try:
            on_message(socket.recv())
        except RuntimeError as e:
            send_message(b"Error on the python backend")
            raise e


def send_message(message):
    socket.send(message)
