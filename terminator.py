import subprocess
import time
from sysman import SystemManager

system_manager = SystemManager()


def process_exists(pid):
    call = 'TASKLIST', '/FI', f'pid eq {pid}'
    output = subprocess.check_output(call)
    last_line = str(output).strip().split('\\r\\n')[-2]
    first_word = last_line.split()[1]
    return first_word == str(pid)


def shut_on_term(args):
    if args.pid is not None:
        shut = 0
        while process_exists(args.pid):
            if not shut:
                print('[*] Bindend, waiting for terminating to shutdown.')
                print('[*] Press CTRL+C to cancel this operation')
            shut = True
            time.sleep(10)
        if shut:
            system_manager.shutdown()