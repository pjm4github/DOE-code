"""
This module handles realtime events such as regular update to the environment, alarms, and processing time limits.
"""

from time import time
from gridlab.gldcore.Globals import FAILED, SUCCESS


class Event:
    def __init__(self, at=0, call=None, next_event=None):
        self.at = at
        self.call = call
        self.next = next_event

starttime = 0
eventlist = Event()


def realtime_run_schedule():
    global eventlist
    global now
    now = realtime_now()
    event = eventlist
    last = None
    while event:
        if event.at <= now:
            call = event.call
            # delete from list */
            if last is None:  # event is first in list
                eventlist = event.next
            else:
                last.next = event.next
            event = None
                # callback */
            if call() is FAILED:
                return FAILED

            # retreat to previous event
            event = last
            if event==None:
                break
            event=event.next
    return SUCCESS


def realtime_schedule_event(at, callback):
    """
    Schedule an event to be executed at a specific time.

    Args:
    at (time_t): Time at which the event is to be scheduled
    callback (function): Callback function to be executed

    Returns:
    Status: Status of the event scheduling
    """
    global eventlist
    event = Event(at, callback, eventlist)
    eventlist = event
    return SUCCESS


def realtime_starttime():
    """
    Get the start time.

    Returns:
    time_t: Start time
    """
    global starttime
    if starttime == 0:
        starttime = realtime_now()
    return starttime


def realtime_now():
    """
    Get the current system time.

    Returns:
    time_t: Current system time
    """
    return int(time())


def realtime_runtime():
    """
    Get the runtime.

    Returns:
    time_t: Runtime
    """
    global starttime
    return realtime_now() - starttime