import time
import zmq
from utilities import Event

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

on_message = Event()


def start_server():
    while True:
        on_message(socket.recv())


def send_message(message):
    socket.send(message)
