from terminator import events, helper
from terminator.observer import observe_process
from terminator.sysman import SystemManager


ACTIONS = {'SHUTDOWN': SystemManager.shutdown, 'ALERT': (lambda: print('Terminated'))}
EVENTS = {'ON_TERMINATE': events.OnTerminateEvent}


def main():
    args = helper.parse_args(ACTIONS.keys(), EVENTS.keys())
    # print(args)

    event = EVENTS[args.event](args.pid)
    observe_process(ACTIONS[args.action], event, verbose=args.verbose is not None)


if __name__ == '__main__':
    main()
