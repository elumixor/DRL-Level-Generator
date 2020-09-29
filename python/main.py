from layout import bytes2state, action2bytes, bytes2training_data
from server import start_server, on_message, send_message
from DRL import agent


def handle_message(message):
    header = message[0:1].decode()
    data = message[1:]

    if header == 'i':
        action = agent.infer(bytes2state(data))
        send_message(action2bytes(action))
    else:
        agent.train(bytes2training_data(data))  # updates the model
        send_message(b'')


on_message += handle_message
start_server()
