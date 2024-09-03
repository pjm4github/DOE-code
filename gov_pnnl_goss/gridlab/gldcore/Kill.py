import os
import ctypes.wintypes
import ctypes
import threading
import signal

from gridlab.gldcore import Globals
from gridlab.gldcore.Class import DynamicClass

"""
This program provides the same kill functionality that is available to Linux versions.
"""


def handler_stop():
    pass



def kill_stophandler():
    global handler_stop
    handler_stop = 1


def msghandler(param):
    name = "gridlabd." + str(os.getpid()) + "." + str(param)
    hEvent = ctypes.windll.kernel32.CreateEventA(None, True, False, name)
    print(f"creating gridlabd signal handler {param} for process {os.getpid()}")
    INFINITE = 0xFFFFFFFF
    WAIT_OBJECT_0 =  0
    while ctypes.windll.kernel32.WaitForSingleObject(hEvent, INFINITE) == WAIT_OBJECT_0:
        print("windows signal handler activated")
        # raise function not directly callable in Python
        # Add your code to handle the signal here
        ctypes.windll.kernel32.ResetEvent(hEvent)


def kill_starthandler():
    """
    # Example usage
    param = 123
    thread = threading.Thread(target=msghandler, args=(param,))
    thread.start()
    time.sleep(5)  # Let the thread run for a while
        :return:
    """
    try:
        thread1 = threading.Thread(target=msghandler, args=(signal.SIGINT,))
        thread2 = threading.Thread(target=msghandler, args=(signal.SIGTERM,))
        thread1.start()
        thread2.start()
        print("windows message signal handlers started")
    except:
        print("kill handler failed to start")


def kill(pid, sig):
    """
    Send a kill signal to a windows version of GridLAB-D.
    Return 0 on successful completion, -1 on error (e.g., no such signal, no such process).
    :param pid: the window process id
    :param sig: the signal id (see signal.h)
    """

    kernel32 = ctypes.windll.kernel32
    kernel32.OpenEventA.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.c_char_p]
    kernel32.OpenEventA.restype = ctypes.wintypes.HANDLE
    kernel32.SetEvent.argtypes = [ctypes.wintypes.HANDLE]
    kernel32.SetEvent.restype = ctypes.wintypes.BOOL
    kernel32.CloseHandle.argtypes = [ctypes.wintypes.HANDLE]

    name = 'gridlabd.{0}.{1}'.format(pid, sig if sig != 0 else Globals.SIGINT)
    EVENT_MODIFY_STATE = 2
    h_event = kernel32.OpenEventA(EVENT_MODIFY_STATE, False, name)

    if sig == 0:
        pass
    # valid signal needs to be sent
    elif h_event == 0:
        pass
    else:
        kernel32.SetEvent(h_event)
        print(f"signal {sig} sent to gridlabd process {pid}")
        kernel32.CloseHandle(h_event)
        return 0
