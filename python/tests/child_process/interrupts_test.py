import signal

interrupted = False


def signal_handler(signal, frame):
    # exit(0)
    global interrupted
    interrupted = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print("started")
while not interrupted:
    pass

print("stopped")
