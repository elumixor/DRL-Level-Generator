try:
    import sys

    sys.path.append('C:\\dev\\DRL-Level-Generator\\python\\src')

    import serialization
    from communication import Server, RequestType, ResponseType

    # if __name__ == '__main__':
    #     def handle_message(server: Server, request_type: RequestType, data: bytes):
    #         if request_type == RequestType.Echo:
    #             command, bytes_read = serialization.to_string(data)
    #             print(command)
    #             if command == "echo":
    #                 server.send_message(ResponseType.Ok, serialization.to_bytes(command))
    #                 return
    #
    #             if command == "stop":
    #                 server.stop()
    #                 return
    #
    #         print(sys.argv[1])
    #         server = Server(sys.argv[1], handle_message)
    #         server.start()
    #         server.wait_for_stop()
    #         print("server stopped")
except BaseException as e:
    print(e)
