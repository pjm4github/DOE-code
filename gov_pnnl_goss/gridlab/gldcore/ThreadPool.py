import threading
import time
import datetime
import os
from queue import Queue

from gridlab.gldcore.Globals import global_threadcount


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
    if os.name in ['nt', 'os2', 'ce']:
        return int(os.environ.get('NUMBER_OF_PROCESSORS', '1'))
    return 1


class ThreadPool:
    def __init__(self, name="", task_function=None, num_threads=0):
        self.num_threads = num_threads
        self.task_function = task_function
        self.tasks = Queue()
        self.threads = []
        self.shutdown_event = threading.Event()
        self.start_cond = threading.Condition()
        self.stop_cond = threading.Condition()
        self.active_threads = 0
        self.name = name
        self.start_lock = threading.Lock()
        # self.start_count = 0
        self.stop_lock = threading.Lock()
        # self.stop_count = 0
        self.debug_mode = True
        self.input = self.task_function.set(None, None)
        self.output = self.task_function.set(None, None)
        self.runtime = 0
        self.n_processes = global_threadcount
        self.process = None

    def get_thread_ids(self):
        ids = []
        for t in self.threads:
            ids.append(t.native_id)
        return ids

    def worker(self):
        while not self.shutdown_event.is_set():
            with self.start_cond:
                self.start_cond.wait()

            while not self.tasks.empty():
                task = self.tasks.get()
                if task is None:
                    break

                # Processing the task
                self.task_function(task)

                with self.stop_cond:
                    self.active_threads -= 1
                    if self.active_threads == 0:
                        self.stop_cond.notify_all()

    def start(self):
        # Create and start threads
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.worker)
            t.start()

            self.threads.append(t)

    def stop(self):
        self.shutdown_event.set()
        for _ in range(self.num_threads):
            self.tasks.put(None)
        for t in self.threads:
            t.join()

    def run_tasks(self, tasks):
        # Reset the event
        self.shutdown_event.clear()

        # Lock to update task queue and active thread count
        with self.start_cond:
            for task in tasks:
                self.tasks.put(task)
                self.active_threads += 1

            self.start_cond.notify_all()  # Start all workers

        with self.stop_cond:
            self.stop_cond.wait_for(lambda: self.active_threads == 0)

    def run(self, result, mti, input_data):
        t0 = time.clock()
        self.task_function.set(result, None)

        # no update required
        if self.task_function.reject(mti, input_data):
            self.debug(mti, "no iteration update required")
            self.task_function.set(result, mti.output)
            return 1

        # single threaded update
        if self.n_processes < 2:
            self.debug(mti, "iterating single threaded")
            return 0

        # multi threaded update
        else:
            self.debug(mti, "starting %d iterators" % mti.n_processes)

            # lock access to stop condition
            self.stop_lock.acquire()

            # reset the stop condition
            self.stop.count = self.n_processes

            # lock access to the start condition
            self.start_lock.acquire()

            # set start condition
            self.task_function.set(mti.input, input_data)
            self.task_function.set(mti.output, None)

            # broadcast start condition
            self.start_cond.notify_all()

            # unlock access to start condition
            self.start_lock.release()

            # wait for stop condition
            while self.stop.count > 0:
                self.stop_cond.wait()

            # unlock access to stop condition
            self.stop_lock.release()

            # gather result
            self.task_function.gather(result, mti.output)
            self.debug(mti, "%d iterators completed" % mti.n_processes)

        self.runtime += time.clock() - t0
        return 1

    def debug(self, fmt, *args):
        if self.debug_mode:
            len = 0
            ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            args_str = ' '.join(map(str, args))
            print(f"MTIDEBUG [{ts}] {self.name if self.name else '(init)'} : {fmt} {args_str}")


# Example task function
def process_task(task):
    print(f"Processing {task}")
    time.sleep(1)

# Example usage
if __name__ == "__main__":
    num_threads = 4
    tasks = [f"Task {i}" for i in range(10)]

    pool = ThreadPool("", num_threads, process_task)
    pool.start()
    pool.run_tasks(tasks)
    pool.stop()
