import time
from terminator.events import Event
from typing import Callable
from terminator.utils.logger import Logger

logger = Logger()


def observe_process(action: Callable, event: Event) -> None:
    """
    This function observes a given process through an event and when it fires an action is performed.
    :param action: action to perform when the event fires
    :param event: the event that fires the action to perform
    """
    try:
        if event():
            action()
        else:
            logger.log('[!] Process not found')
    except KeyboardInterrupt:
        logger.log('[!] Operation cancelled.')
