import os
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import threading
import queue
import time
import sys

class CppThreadPool:
    """
    # Example usage:
        def example_job(index):
            print(f"Job {index} executed by thread {threading.current_thread().ident}")

        num_threads = 4
        pool = PythonThreadPool(num_threads)

        for i in range(10):
            pool.add_job(lambda i=i: example_job(i))

        pool.await()

        # Getting the thread map
        thread_map = pool.get_threadmap()
        print("Thread Map:")
        for thread_id, index in thread_map.items():
            print(f"Thread {index}: ID {thread_id}")

        # Clean up
        pool.exiting = True
        with pool.condition:
            pool.condition.notify_all()
        for thread in pool.threads:
            thread.join()
    """
    def __init__(self, num_threads):
        self.running_threads = 0
        self.exiting = threading.Event()
        # self.exiting = False
        self.sync_id = threading.get_ident()
        self.queue = queue.Queue()
        self.job_queue = queue.Queue()
        self.queue_lock = threading.Lock()
        self.wait_lock = threading.Lock()
        self.sync_mode = False
        self.condition = threading.Condition()
        self.sync_condition = threading.Condition()
        self.shutdown_id = None
        self.threads = [threading.Thread(target=self.worker) for _ in range(num_threads)]
        for t in self.threads:
            t.start()

    def sync_wait_on_queue(self):
        with self.wait_lock:
            while not self.job_queue.empty():
                time.sleep(0.1)

    def wait_on_queue(self):
        with self.wait_lock:
            while self.running_threads > 0:
                time.sleep(0.1)

    def set_sync_mode(self, mode):
        self.sync_mode = mode



    # def await(self):
    #     if self.sync_mode:
    #         self.sync_wait_on_queue()
    #     else:
    #         self.wait_on_queue()

    def get_threadmap(self):
        thread_map = {}
        for i, thread in enumerate(self.threads):
            thread_map[thread.ident] = i
        return thread_map

    def __del__(self):
        self.exiting.set()
        self.sync_mode = True
        self.add_job(lambda: None)
        self.sync_mode = False
        for thread in self.threads:
            if thread.is_alive():
                self.add_job(lambda: None)
        for thread in self.threads:
            thread.join()

        for t in self.threads:
            t.join()

    def async_wait_on_queue(self):
        with self.queue_lock:
            while not self.job_queue.empty() or self.running_threads > 0:
                if self.sync_mode:
                    self.sync_condition.wait()
                else:
                    self.condition.wait()
        # if self.sync_mode:
        #     raise RuntimeError("Sync mode is already active")
        # while not self.queue.empty():
        #     time.sleep(0.1)

    def await_on_queue(self):
        with self.queue_lock:
            while self.job_queue.empty() and self.running_threads > 0:
                if self.sync_mode:
                    self.sync_condition.wait()
                else:
                    self.condition.wait()
        # if not self.sync_mode:
        #     raise RuntimeError("Sync mode is not active")
        # while not self.queue.empty():
        #     time.sleep(0.1)

    def add_job(self, job):
        with self.queue_lock:
            try:
                self.running_threads += 1
                self.job_queue.put(job)
                if self.sync_mode:
                    self.sync_condition.notify()
                else:
                    self.condition.notify()
                return True
            except Exception:
                pass

    # def add_job(self, job):
    #     if self.exiting:
    #         return False
    #
    #     with self.queue_lock:
    #         self.job_queue.put(job)
    #
    #     with self.condition:
    #         self.condition.notify()
    #
    #     return True

    #
    # def await(self):
    #     with self.queue_lock:
    #         while self.running_threads > 0:
    #             if self.sync_mode:
    #                 self.sync_condition.wait()
    #             else:
    #                 self.condition.wait()

    def worker(self):
        while not self.exit_flag:
            try:
                job = self.job_queue.get(timeout=1)
                job()
            except queue.Empty:
                pass
            finally:
                with self.queue_lock:
                    self.running_threads -= 1
                    if self.sync_mode and self.job_queue.empty():
                        self.sync_condition.notifyAll()
                    elif not self.sync_mode and self.job_queue.empty():
                        self.condition.notifyAll()
        #
        # while not self.exiting.is_set():
        #     try:
        #         job = self.queue.get(timeout=0.1)
        #         job()
        #     except queue.Empty:
        #         continue
        #     except Exception as e:
        #         sys.stderr.write("Exception in worker thread: {}\n".format(e))
        #     finally:
        #         with self.queue_lock:
        #             self.running_threads -= 1
        #             self.queue.task_done()


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
class cpp_threadpool:
    def __init__(self, num_threads):
        if num_threads == 0:
            num_threads = os.cpu_count()
            
        self.sync_mode = False  # Default to parallel
        self.sync_id = None
        self.Threads = []

        local_thread = threading.Thread(target=self.sync_wait_on_queue)
        local_thread.start()
        self.sync_id = local_thread.ident
        self.Threads.append(local_thread)

        for index in range(num_threads):
            local_thread = threading.Thread(target=self.wait_on_queue)
            local_thread.start()
            self.Threads.append(local_thread)
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
def sync_wait_on_queue(self):
    job = None
    with self.queue_lock:
        while not self.exiting:
            if not self.queue_lock.locked():
                self.queue_lock.acquire()
            self.sync_condition.wait(self.queue_lock, lambda: not self.job_queue.empty())
            if self.job_queue.empty():
                continue
            else:
                job = self.job_queue.front()
                self.job_queue.pop()
            self.queue_lock.release()
            job()  # function type
            self.wait_condition.notify_all()
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
def wait_on_queue(self):

    def job():
        pass

    with self.queue_lock:

        while not self.exiting.load() and not threading.get_ident() == self.shutdown_id:
            if not self.queue_lock.owned_lock:
                self.queue_lock.acquire()
            self.condition.wait_for(lambda: not self.job_queue.empty())

            with self.sync_mode_lock:
                if self.job_queue.empty():
                    continue
                else:
                    job = self.job_queue[0]
                    self.job_queue = self.job_queue[1:]

            self.queue_lock.release()
            job()
            self.running_threads -= 1
            self.wait_condition.notify_all()

    #     job = None
    #     with self.queue_lock:
    #         while (not self.exiting and
    #                not threading.current_thread().ident == self.shutdown_id):
    #             if not self.queue_lock.owns_lock():
    #                 self.queue_lock.acquire()
    #             self.condition.wait(self.queue_lock,
    #                                lambda: not self.job_queue.empty())
    #             with self.sync_mode_lock:
    #                 if self.job_queue.empty():
    #                     continue
    #                 else:
    #                     job = self.job_queue.front()
    #                     self.job_queue.pop()
    #             self.queue_lock.release()
    #             job()  # function<void()> type
    #             self.running_threads -= 1
    #             self.wait_condition.notify_all()
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 

def await_(self):
    with self._wait_lock:
        self._wait_condition.wait_for(self._lock, 50, lambda: self._running_threads.load() <= 0)