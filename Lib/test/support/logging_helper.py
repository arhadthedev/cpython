import logging.handlers
from  test import support
from sys import stdout

class TestHandler(logging.handlers.BufferingHandler):
    def __init__(self, matcher):
        # BufferingHandler takes a "capacity" argument
        # so as to know when to flush. As we're overriding
        # shouldFlush anyway, we can set a capacity of zero.
        # You can call flush() manually to clear out the
        # buffer.
        logging.handlers.BufferingHandler.__init__(self, 0)
        self.matcher = matcher

    def shouldFlush(self):
        return False

    def emit(self, record):
        self.format(record)
        self.buffer.append(record.__dict__)

    def matches(self, **kwargs):
        """
        Look for a saved dict whose keys/values match the supplied arguments.
        """
        result = False
        for d in self.buffer:
            if self.matcher.matches(d, **kwargs):
                result = True
                break
        return result


def verbose(func):
    """A decorator providing a logging function for tests."""
    def wrapper(*args, **kwargs):
        if support.verbose:
            stdout.write('\n')

        def log(message, role=None):
            if support.verbose:
                prefix = f' {role}: ' if role else ''
                stdout.write(f'{prefix}{message}\n')
        return func(*args, log=log, **kwargs)

    return wrapper
