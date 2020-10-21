from communication.server_exception import ServerException

try:
    import argparse
    import sys
    import traceback


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
    from configuration import TrainingConfiguration
    import serialization
    from training_controller import TrainingController

    training_controller = None


    def handle_message(server: Server, request_type: RequestType, data: bytes):
        try:
            global training_controller
            if request_type == RequestType.WakeUp:
                server.send_ok()
                return

            if request_type == RequestType.SendConfiguration:
                configuration = TrainingConfiguration(data, 0)
                training_controller = TrainingController(configuration)
                server.send_ok(training_controller.actor_byte_data)
                return

            if request_type == RequestType.SendTrainingData:
                training_controller.train(data, 0)
                server.send_ok(training_controller.actor_byte_data)
                return

            if request_type == RequestType.ShutDown:
                server.send_ok()
                server.stop()
                return

            raise ServerException("Unsupported request type")
        except Exception as e:
            traceback.print_exc()
            try:
                server.send_failure(serialization.to_bytes(str(e)))
            except Exception as e:
                print("Could not send error response", file=sys.stderr)
                print(e, file=sys.stderr)

            server.stop()
            print("Press [Enter] to continue...")
            input()


    server = Server(address, handle_message)
    server.start()
    server.wait_for_stop()

except Exception:
    traceback.print_exc()
    print("Press [Enter] to continue...")
    input()
