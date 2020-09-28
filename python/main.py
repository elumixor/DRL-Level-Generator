import struct

from server import start_server, on_message, send_message


def handle_message(bytes):
    header = bytes[0:1].decode()
    data = struct.unpack('f', bytes[1:])[0]

    response = 0 if data > 1 else 1

    send_message(struct.pack('i', response))


on_message += handle_message
start_server()
