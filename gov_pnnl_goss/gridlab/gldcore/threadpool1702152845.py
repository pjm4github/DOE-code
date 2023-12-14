import threading
import time
import datetime
import os


class MtiFunctions:
    def get(self, item):
        return None
    
    def set(self, data1, data2):
        return None

class Mti:
    def __init__(self, name, fn, min_items):
        self.name = name
        self.fn = fn
        self.start_cond = threading.Condition()
        self.start_lock = threading.Lock()
        self.start_count = 0
        self.stop_cond = threading.Condition()
        self.stop_lock = threading.Lock()
        self.stop_count = 0
        self.input = self.fn.set(None, None)
        self.output = self.fn.set(None, None)
        self.runtime = 0
        self.n_processes = global_threadcount
        self.process = None

    def iterator_proc(self, tp):
        mti = tp.mti
        final = mti.fn.set(None, None)
        while tp.enabled:
            pass
        free(final)
        return 0
    
    def mti_run(self, result, input):
        pass
    
def mti_debug(mti, fmt, *args):
    pass

def processor_count():
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass
    if os.name == 'posix':
        try:
            return os.sysconf('SC_NPROCESSORS_ONLN')
        except (AttributeError, ValueError):
            pass
        try:
            return int(os.popen2('sysctl -n hw.ncpu')[1].read())
        except (AttributeError, ValueError):
            pass
    if os.name in ['nt', 'os2', 'ce']:
        return int(os.environ.get('NUMBER_OF_PROCESSORS', '1'))
    return 1


def mti_debug(mti, fmt, *args):
    if mti_debug_mode:
        len = 0
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        args_str = ' '.join(map(str, args))
        print(f"MTIDEBUG [{ts}] {mti.name if mti else '(init)'} : {fmt} {args_str}")
        len += len(fmt) + len(args_str) + len(ts) + len(mti.name if mti else '(init)') + 21
        return len
    return 0


def processor_count():
    return get_nprocs()



def processor_count():
    count = os.sysctl("hw.ncpu")
    if not count:
        return 1
    return count


def processor_count():
    if os.name == 'nt':
        import psutil
        return psutil.cpu_count()
    else:
        proc_count = os.getenv("NUMBER_OF_PROCESSORS")
        count = int(proc_count) if proc_count else 0
        return count if count else 1


def mti_run(result, mti, input_data):
    t0 = time.clock()
    mti.fn.set(result, None)

    # no update required
    if mti.fn.reject(mti, input_data):
        mti_debug(mti, "no iteration update required")
        mti.fn.set(result, mti.output)
        return 1

    # single threaded update
    if mti.n_processes < 2:
        mti_debug(mti, "iterating single threaded")
        return 0

    # multi threaded update
    else:
        mti_debug(mti, "starting %d iterators" % mti.n_processes)

        # lock access to stop condition
        mti.stop.lock.acquire()

        # reset the stop condition
        mti.stop.count = mti.n_processes

        # lock access to the start condition
        mti.start.lock.acquire()

        # set start condition
        mti.fn.set(mti.input, input_data)
        mti.fn.set(mti.output, None)

        # broadcast start condition
        mti.start.cond.notify_all()

        # unlock access to start condition
        mti.start.lock.release()

        # wait for stop condition
        while mti.stop.count > 0:
            mti.stop.cond.wait()

        # unlock access to stop condition
        mti.stop.lock.release()

        # gather result
        mti.fn.gather(result, mti.output)
        mti_debug(mti, "%d iterators completed" % mti.n_processes)

    mti.runtime += time.clock() - t0
    return 1
