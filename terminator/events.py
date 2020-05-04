import abc
import time
from terminator.sysman import SystemManager
from terminator.utils.logger import Logger

logger = Logger()
system_manager = SystemManager()

BUSY_WAIT_DURATION = 1


class Event(abc.ABC):
    """
    This class represents the abstract concept of Event.
    """
    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class OnTerminateEvent(Event):
    """
    This Event is return True when a given process terminates.
    """
    def __init__(self, pid):
        self._pid = pid

    def __call__(self, *args, **kwargs):
        found = False
        while system_manager.process_exists(self._pid):
            if not found:
                logger.log('[*] Process found')
                logger.log('[*] Press CTRL+C to cancel this operation')
            found = True
            time.sleep(BUSY_WAIT_DURATION)
        return found
