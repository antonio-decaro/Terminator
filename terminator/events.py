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

    def __bool__(self):
        return self()


class OnTerminateEvent(Event):
    """
    This Event is return True when a given process terminates.
    """
    def __init__(self, pid):
        self._pid = pid

    def __call__(self, *args, **kwargs):
        try:
            found = False
            while system_manager.process_exists(self._pid):
                if not found:
                    logger.log(f'[+] Process {self._pid} found. Waiting for process to terminate')
                found = True
                time.sleep(BUSY_WAIT_DURATION)
            if not found:
                logger.log(f'[!] Process {self._pid} not found')
            else:
                logger.log(f'[-] Process {self._pid} terminated')
            return found
        except KeyboardInterrupt:
            print('alfredo')


class OnStartEvent(Event):
    """
        This Event is return True when a given process starts.
    """

    def __init__(self, pid):
        self._pid = pid

    def __call__(self, *args, **kwargs):
        found = False
        while not system_manager.process_exists(self._pid):
            if not found:
                logger.log(f'[*] Attempting to find process {self._pid}')
                logger.log(f'[*] Press CTRL+C to cancel this operation')
            found = True
            time.sleep(BUSY_WAIT_DURATION)
        return found
