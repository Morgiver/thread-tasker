import concurrent.futures
import threading

class ThreadTasker:
    """ Thread Tasker managing and executing tasks"""
    def __init__(self, max_workers=4):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, task_fn, **kwargs):
        return self.executor.submit(task_fn, **kwargs)

    def shutdown(self, wait=True):
        self.executor.shutdown(wait=wait)

class Server:
    def __init__(self):
        self.stop_event = None
        self.server_future = None
        self.run_arguments = {}

    def loop(self, tasker, **kwargs):
        self.on_start()
        while not self.stop_event.is_set():
            self.on_step()

        self.on_stop()

    def start(self, tasker: ThreadTasker):
        self.stop_event = threading.Event()
        self.server_future = tasker.submit(lambda: self.loop(tasker, **self.run_arguments))

    def stop(self):
        self.stop_event.set()
        return self.server_future.result()

    def on_start(self):
        pass

    def on_step(self):
        pass
