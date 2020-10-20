import argparse
import sys


def get_args(*keys):
    parser = argparse.ArgumentParser()
    for key in keys:
        parser.add_argument(f'--{key}')

    args = vars(parser.parse_args())
    return [args.get(key) for key in keys]


[working_directory, address] = get_args("working_directory", "address")
sys.path.append(working_directory)

# Custom import should occur after appending the working directory fo path,
# which is required when launching from C# to resolve imports correctly
# when the file is not under the root (src) directory
from communication import Server, RequestType
import serialization

configuration = None


def handle_message(server: Server, request_type: RequestType, data: bytes):
    if request_type == RequestType.Echo:
        t, bytes_read = serialization.to_string(data)

        if t == "int":
            value = serialization.to_int(data, bytes_read)
            server.send_ok(serialization.to_bytes(value))
            return

        if t == "float":
            value = serialization.to_float(data, bytes_read)
            server.send_ok(serialization.to_bytes(value))
            return

        if t == "string":
            value, bytes_read = serialization.to_string(data, bytes_read)
            server.send_ok(serialization.to_bytes(value))
            return

        if t == "list_int":
            value, bytes_read = serialization.to_list_int(data, bytes_read)
            server.send_ok(serialization.to_bytes(value))
            return

        if t == "list_float":
            value, bytes_read = serialization.to_list_float(data, bytes_read)
            server.send_ok(serialization.to_bytes(value))
            return

        if t == "tensor":
            value, bytes_read = serialization.to_tensor_float(data, bytes_read)
            server.send_ok(serialization.to_bytes(value))
            return

        if t == "state_dict":
            value, bytes_read = serialization.to_state_dict(data, bytes_read)
            server.send_ok(serialization.to_bytes(value))
            return

        server.send_failure(serialization.to_bytes(f"Unknown type: {t}"))
        return

    if request_type == RequestType.ShutDown:
        server.send_ok()
        server.stop()


server = Server(address, handle_message)
server.start()
server.wait_for_stop()
