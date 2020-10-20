from communication import Server, RequestType


def handle_message(server: Server, request_type: RequestType, data: bytes):
    pass


if __name__ == '__main__':
    server = Server("tcp://*:5555", handle_message)
    server.start()
    server.wait_for_stop()

