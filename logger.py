from threading import Lock
from typing import Optional


class Logger:
    _instance: Optional['Logger'] = None
    _lock: Lock = Lock()

    def __new__(cls) -> 'Logger':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, message: str) -> None:
        print(f"[LOG]: {message}")
