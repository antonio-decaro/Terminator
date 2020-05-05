from terminator import events, helper
from terminator.observer import observe_process
from terminator.sysman import SystemManager
from terminator.utils.logger import Logger

logger = Logger()
system_manager = SystemManager()

ACTIONS = {'SHUTDOWN': system_manager.shutdown, 'ALERT': (lambda: print('!!! ALERT !!! ALERT !!! ALERT !!!'))}
EVENTS = {'ON_TERMINATE': events.OnTerminateEvent, 'ON_START': events.OnStartEvent}
MODE = ['ALL', 'ANY']


def main():
    args = helper.parse_args(ACTIONS.keys(), EVENTS.keys(), MODE)
    logger.enabled = args.verbose is not None

    logger.log(f'[*] Looking for process: {args.pid}')
    logger.log(f'[*] Selected mode: {args.mode}')

    mode = any if args.mode == 'ANY' else all
    event_list = [EVENTS[args.event](pid) for pid in args.pid]
    observe_process(ACTIONS[args.action], mode, *event_list)


if __name__ == '__main__':
    main()
