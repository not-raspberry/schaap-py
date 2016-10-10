"""Statistical profiling utility."""
import signal
from time import time
from contextlib import contextmanager

DEFAULT_DELAY = 1
DEFAULT_INTERVAL = 0.01


def get_frame_location(frame):
    """
    Extract information useful for profiling from the frame.

    In one Python module there may be multiple functions with the same name.
    That's why we attach function line to function name.

    :param frame frame:
    :rtype: tuple
    :return: a 3-tuple of:
        - module name, e.g. 'prompt_toolkit.layout.containers'
        - function name or Class.method name, e.g. '1184:Window._copy_body'
        - current line number, int
    """
    function_name = frame.f_code.co_name
    try:
        # `self` isn't a keyword. The name of the first argument of a method is arbitrary.
        # But that's the least wrong way to get a class form a frame.
        class_name = frame.f_locals['self'].__class__.__name__
    except (KeyError, AttributeError):
        function_id = function_name
    else:
        function_id = '{}.{}'.format(class_name, function_name)

    return (frame.f_globals['__name__'], function_id, frame.f_lineno)


def frame_to_trace(frame):
    """
    Create a backtrace list from the topmost frame.

    Most recent call last.

    :param frame frame:
    :rtype: list
    :return: list of 3-tuples with location within frames
    """
    trace = []
    while True:
        if frame is not None:
            trace.append(get_frame_location(frame))
            frame = frame.f_back
        else:
            trace.reverse()
            return trace


def push(timestamp, trace):
    """
    Send the trace away.

    :param float timestamp: a timestamp, returned by time.time()
    :param float:
    """
    print trace


def handle(number, frame):
    """Profiling signal handler."""
    trace = frame_to_trace(frame)
    push(time(), trace)


def hook(interval=DEFAULT_INTERVAL, delay=DEFAULT_DELAY):
    """
    Install the profiling signal handler and tell the kernel to send SIGPROF repeatedly.

    :param float delay: delay before the first profiling signal, in seconds
    :param float interval: SIGPROF interval, in seconds
    """
    signal.signal(signal.SIGPROF, handle)
    signal.setitimer(signal.ITIMER_PROF, delay, interval)


def unhook():
    """
    Clear the signal handler and the profiling alarm.

    If the alarm is not cleared, CPython may be killed when shutting down.
    """
    signal.setitimer(signal.ITIMER_PROF, 0)
    signal.signal(signal.SIGPROF, signal.SIG_DFL)


@contextmanager
def profiling(*args, **kwargs):
    """
    A context manager to arm and disarm profiling.

    Arguments are passed to the `hook` function. Does not nest.
    """
    hook(*args, **kwargs)
    try:
        yield
    finally:
        unhook()
