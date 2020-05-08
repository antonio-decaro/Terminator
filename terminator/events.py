import abc
import time
from terminator.sysman import SystemManager
from terminator.utils.logger import Logger

logger = Logger()
system_manager = SystemManager()

BUSY_WAIT_DURATION = 1

stop = False


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
    def __init__(self, idd):
        self._idd = idd

    def __call__(self, *args, **kwargs):
        found = False
        while system_manager.process_exists(self._idd) and not stop:
            if not found:
                logger.log(f'[+] Process {self._idd} found. Waiting for process to terminate')
            found = True
            time.sleep(BUSY_WAIT_DURATION)
        if stop:
            return False
        if not found:
            logger.log(f'[!] Process {self._idd} not found')
        else:
            logger.log(f'[-] Process {self._idd} terminated')
        return found


class OnStartEvent(Event):
    """
        This Event is return True when a given process starts.
    """

    def __init__(self, idd):
        self._idd = idd

    def __call__(self, *args, **kwargs):
        found = False
        while not system_manager.process_exists(self._idd) and not stop:
            if not found:
                logger.log(f'[*] Attempting to find process {self._idd}')
            found = True
            time.sleep(BUSY_WAIT_DURATION)
        if stop:
            return False
        if found:
            logger.log(f'[+] Process {self._idd} found')
        if not found:
            logger.log(f'[!] Process {self._idd} already started')
        return found


def stop_all():
    global stop
    stop = True
