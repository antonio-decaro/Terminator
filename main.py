from terminator import events, helper
from terminator.observer import observe_process
from terminator.sysman import SystemManager
from terminator.utils.logger import Logger

logger = Logger()
system_manager = SystemManager()

ACTIONS = {'SHUTDOWN': system_manager.shutdown, 'ALERT': (lambda: print('Terminated'))}
EVENTS = {'ON_TERMINATE': events.OnTerminateEvent}


def main():
    args = helper.parse_args(ACTIONS.keys(), EVENTS.keys())

    logger.enabled = args.verbose is not None

    event = EVENTS[args.event](args.pid)
    observe_process(ACTIONS[args.action], event)


if __name__ == '__main__':
    main()
