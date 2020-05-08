import os
import subprocess
import platform
import abc
from typing import List, Tuple


class _System(abc.ABC):
    @abc.abstractmethod
    def shutdown(self) -> None:
        pass

    @abc.abstractmethod
    def process_exists(self, pid: Tuple[int, str]) -> bool:
        pass

    @abc.abstractmethod
    def get_pid(self, name: str) -> List[int]:
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

    def shutdown(self) -> None:
        return self.__instance.shutdown()

    def process_exists(self, pid: Tuple[int, str]) -> bool:
        return self.__instance.process_exists(pid)

    def get_pid(self, name: str) -> List[int]:
        return self.__instance.get_pid(name)


class _WindowsSystem(_System):
    class Task:
        def __init__(self, imgname, pid, session_name, session_number, mem_use):
            self.imgname = imgname
            self.pid = pid
            self.session_name = session_name
            self.session_number = session_number
            self.mem_use = mem_use

        def __repr__(self):
            return f'{self.imgname=} {self.pid=} {self.session_name=} {self.session_number=} {self.mem_use=}'

        __str__ = __repr__

        @staticmethod
        def from_string(raw_str: str):
            vals = raw_str.split()
            return _WindowsSystem.Task(vals[0], int(vals[1]), vals[2], vals[3], ''.join(vals[4:]))

    def shutdown(self) -> None:
        os.system('shutdown /s /f /t 60')

    def process_exists(self, idd: Tuple[int, str]) -> bool:
        is_pid = isinstance(idd, int)
        call = ('TASKLIST', '/FI', f'pid eq {idd}') if is_pid else ('TASKLIST', '/FI', f'imagename eq {idd}')
        output = subprocess.check_output(call)
        last_line = str(output).strip().split('\\r\\n')[-2]
        first_word = last_line.split()[1 if is_pid else 0]
        return first_word == str(idd)

    def get_pid(self, name: str) -> List[int]:
        call = 'TASKLIST', '/FI', f'imagename eq {name}'
        output = subprocess.check_output(call)
        lines = output.decode('unicode_escape').strip().split('\r\n')[2:]
        tasks = [self.Task.from_string(line) for line in lines]
        return [task.pid for task in tasks if name in task.imgname]


class _LinuxSystem(_System):
    def shutdown(self):
        raise NotImplementedError

    def process_exists(self, pid: Tuple[int, str]) -> bool:
        raise NotImplementedError

    def get_pid(self, name: str) -> List[int]:
        raise NotImplementedError
