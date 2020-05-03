import argparse
from terminator import shut_on_term


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pid', type=int, help='The PID of the process to wait')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    shut_on_term(args)
