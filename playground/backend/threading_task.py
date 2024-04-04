import threading
import time

def _task(interval: float):
    while True:
        time.sleep(interval)


def start_threading_task(interval: float):
    thread = threading.Thread(target=_task, args=(interval,))
    thread.start()
