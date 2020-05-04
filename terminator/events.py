import abc
import subprocess


class Event(abc.ABC):
    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class OnTerminateEvent(Event):
    def __init__(self, pid):
        self._pid = pid

    def __call__(self, *args, **kwargs):
        return process_exists(self._pid)


def process_exists(pid) -> bool:
    call = 'TASKLIST', '/FI', f'pid eq {pid}'
    output = subprocess.check_output(call)
    last_line = str(output).strip().split('\\r\\n')[-2]
    first_word = last_line.split()[1]
    return first_word == str(pid)

