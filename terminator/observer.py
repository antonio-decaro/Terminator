import time
from terminator.events import Event
from typing import Callable


def observe_process(action: Callable, event: Event, /, *, verbose: bool = False) -> None:
    executed = 0
    try:
        while event():
            if not executed and verbose:
                print('[*] Bindend, waiting for terminating to shutdown.')
                print('[*] Press CTRL+C to cancel this operation')
            executed = True
            time.sleep(2)
        if executed:
            action()
    except KeyboardInterrupt:
        if verbose:
            print('[!] Cancelled.')
