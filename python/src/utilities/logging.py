from datetime import datetime


def log(message):
    time = datetime.now().strftime("[%H:%M:%S]")
    print(f"{time} {message}")
