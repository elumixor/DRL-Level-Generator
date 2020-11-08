from datetime import datetime
from .plotter import Plotter

def log(message):
    time = datetime.now().strftime("[%H:%M:%S]")
    print(f"{time} {message}")