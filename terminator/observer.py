import os
from concurrent import futures
from terminator.events import Event, stop_all
from typing import Callable
from terminator.utils.logger import Logger

logger = Logger()


def observe_process(action: Callable, mode, *events: Event) -> None:
    """
    This function observes a given process through an event and when it fires an action is performed.
    :param action: action to perform when the event fires
    :param mode: the mode to observe processes:
        - any: at least one event must fires
        - all: all events must fire
    :param events: the events that fires the action to perform
    """
    fts = set()
    results = []

    with futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for event in events:
            ft = executor.submit(event)
            fts.add(ft)
        for ft in futures.as_completed(fts):
            results.append(ft.result())
            if mode is any and any(results):
                stop_all()
                executor.shutdown(False)
                break
    if any(results):
        action()
