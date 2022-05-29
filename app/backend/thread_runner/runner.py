from abc import ABC, abstractmethod
from threading import Thread


class ThreadRunner(ABC):

    def __init__(self):
        self._thread = None
        self.is_running = False

    def start(self):
        self.is_running = True
        if not self._thread:
            self._thread = Thread(target=self._run, args=(), daemon=True)
            self._thread.start()

    def stop(self):
        self.is_running = False
        if self._thread:
            self._thread = None

    @abstractmethod
    def _run(self):
        pass
