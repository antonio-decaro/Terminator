import os
import subprocess
import platform
import abc


class _System(abc.ABC):
    @abc.abstractmethod
    def shutdown(self):
        pass

    @abc.abstractmethod
    def process_exists(self, pid):
        pass


class SystemManager(_System):
    """
    This class detects on which system we are executing the python environment.
    """

    __instance = None

    def __init__(self):
        if platform.system() == 'Windows':
            self.__instance = _WindowsSystem()
        elif platform.system() == 'Linux':
            self.__instance = _LinuxSystem()

    def shutdown(self):
        return self.__instance.shutdown()

    def process_exists(self, pid):
        return self.__instance.process_exists(pid)


class _WindowsSystem(_System):
    def shutdown(self):
        os.system('shutdown /s /f /t 60')

    def process_exists(self, pid):
        call = 'TASKLIST', '/FI', f'pid eq {pid}'
        output = subprocess.check_output(call)
        last_line = str(output).strip().split('\\r\\n')[-2]
        first_word = last_line.split()[1]
        return first_word == str(pid)


class _LinuxSystem(_System):
    def shutdown(self):
        os.system('shutdown -t 60')

    def process_exists(self, pid):
        pass
