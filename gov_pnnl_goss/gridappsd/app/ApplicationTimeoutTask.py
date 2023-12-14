
import threading


class ApplicationTimeoutTask(threading.Timer):
    
    def __init__(self, seconds, app_id, timeout_callback):
        super().__init__(0, self.run)
        self.seconds = seconds
        self.app_id = app_id
        self.timeout_callback = timeout_callback
        # self.reset()

    def reset(self):
        timer = threading.Timer(self.seconds, self.run)
        try:
            timer.start()
            # timer.scheduleAtFixedRate(this, 1000, this.seconds*1000);
        except RuntimeError:
            self.cancel()
            timer = threading.Timer(self.seconds, self.run)
            # timer.scheduleAtFixedRate(this, 1000, this.seconds*1000);
            timer.start()

    def run(self):
        print("Timeout not reset in time for", self.app_id)
        self.timeout_callback.timeout(self.app_id)
