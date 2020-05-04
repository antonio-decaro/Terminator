import sys


class Singleton:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance


@Singleton
class Logger:
    def __init__(self, out=sys.stdout, enabled=True):
        self.out = out
        self.enabled = enabled

    def log(self, msg):
        if self.enabled:
            print(msg, file=self.out)
