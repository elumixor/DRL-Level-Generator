try:
    import sys
    import argparse

    import signal

    import time  # For the demo only

    def get_args(*keys):
        parser = argparse.ArgumentParser()
        for key in keys:
            parser.add_argument(f'--{key}')

        ns = parser.parse_args()
        args = vars(ns)
        return [args.get(key) for key in keys]


    [working_directory, address] = get_args("working_directory", "address")
    sys.path.append(working_directory)

    import serialization
    from communication import Server, RequestType, ResponseType

    def handle_message(server: Server, request_type: RequestType, data: bytes):
        if request_type == RequestType.Echo:
            command, bytes_read = serialization.to_string(data)
            print(command)
            if command == "echo":
                server.send_message(ResponseType.Ok, serialization.to_bytes(command))
                return

            if command == "stop":
                server.send_message(ResponseType.Ok)
                server.stop()
                return


    server = Server(address, handle_message)
    server.start()
    server.wait_for_stop()
except BaseException as e:
    print(e)
