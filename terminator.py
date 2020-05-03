import sys
import os
import subprocess
import time
import argparse


SHUTDOWN = 'shutdown /s /f /t 60'


def process_exists(pid):
    call = 'TASKLIST', '/FI', f'pid eq {pid}'
    output = subprocess.check_output(call)
    last_line = str(output).strip().split('\\r\\n')[-2]
    first_word = last_line.split()[1]
    return first_word == str(pid)


def shut_on_term(args):
    if args.pid is not None:
        shut = False
        while process_exists(args.pid):
            if not shut:
                print('[*] Bindend, waiting for terminating to shutdown.')
                print('[*] Press CTRL+C to cancel this operation')
            shut = True
            time.sleep(10)

        if shut:
            os.system(SHUTDOWN)
