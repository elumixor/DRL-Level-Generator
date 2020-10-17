from layout import bytes2state, action2bytes, bytes2training_data
from server import start_server, on_message, send_message
from DRL import Agent
from utilities import log


def handle_message(message):
    # Parse message
    header = message[0:1].decode()
    data = message[1:]

    if header == 'i':
        # log(f"Received inference request ({len(data)}B)")
        state = bytes2state(data)
        action = Agent.infer(state)
        send_message(action2bytes(action))
    else:
        log(f"Received training request ({len(data)}B)")
        training_data = bytes2training_data(data)
        Agent.train(training_data)  # updates the model
        send_message(b'')


on_message += handle_message
start_server()
