import argparse

DESCRIPTION = """
This python script help to observing a system process, and doing some actions when their state changes.
"""

ACTION_DESCRIPTION = """
an action to execute when the event fires.
    (SHUTDOWN - shutdowns the computer |
    ALERT - prints 'Terminated')
"""

EVENT_DESCRIPTION = """
the event is when the action has to be performed.
    (ON_TERMINATE - when the process terminates) | 
    (ON_START - when the process starts; not recommended with -p)
"""

MODE_DESCRIPTION = """
ANY (default) - at least one process must fire | ALL - all processes must fire
"""


def parse_args(actions, events, mode):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('action', metavar='ACTION', choices=actions, help=ACTION_DESCRIPTION)
    parser.add_argument('event', metavar='EVENT', choices=events, help=EVENT_DESCRIPTION)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--pid', metavar='PID', nargs='+', type=int, help='the PID of the process to observe')
    group.add_argument('-n', '--name', metavar='NAME', nargs='+', type=str, help='the name of the process to observe')
    parser.add_argument('--mode', choices=mode, default='ANY', help=MODE_DESCRIPTION)
    parser.add_argument('-v', '--verbose', action='count', help='enable the verbosity')
    return parser.parse_args()
