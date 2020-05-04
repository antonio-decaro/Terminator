import argparse

DESCRIPTION = """
This python script help to observing a system process, and doing some actions when their state changes.
"""


def parse_args(actions, events):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('action', metavar='ACTION', choices=actions, help='An action to execute on an event')
    parser.add_argument('event', metavar='EVENT', choices=events, help='When execute the action')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--pid', metavar='PID', type=int, help='The PID of the process to observe')
    group.add_argument('-n', '--name', metavar='NAME', type=str, help='The name of the process to observe')
    parser.add_argument('-v', '--verbose', action='count', help='Enable the verbosity')
    return parser.parse_args()