import os
import platform
import abc


class _System(abc.ABC):
    @abc.abstractmethod
    def shutdown(self):
        pass


class SystemManager(_System):
    """
    This class detects on which system we are executing the python environment.
    """
    __instance = None

    def __init__(self):
        if platform.system() == 'WINDOWS':
            self.__instance = _WindowsSystem()
        elif platform.system() == 'Linux':
            self.__instance = _LinuxSystem()

    def shutdown(self):
        return self.__instance.shutdown()


class _WindowsSystem(_System):
    def shutdown(self):
        os.system('shutdown /s /f /t 60')


class _LinuxSystem(_System):
    def shutdown(self):
        os.system('shutdown -t 60')
