import time
import _thread


def watchdog_timer(state, wait=3):
    """Interrupts the main thread if time limit is reached
    Original code: https://stackoverflow.com/questions/37412234/timeout-function-if-it-takes-too-long
    """
    time.sleep(wait)
    if not state['completed']:
        _thread.interrupt_main()
