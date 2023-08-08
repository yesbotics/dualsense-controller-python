from threading import Lock
from typing import Generic, Final

from dualsense_controller.core.typedef import LockableValue


class Lockable(Generic[LockableValue], object):
    __slots__ = ['_value', '_lock']

    @property
    def value(self) -> LockableValue | None:
        with self._lock:
            return self._value

    @value.setter
    def value(self, value: LockableValue | None) -> None:
        with self._lock:
            self._value = value

    def __init__(self, lock: Lock = None, value: LockableValue = None):
        self._lock: Final[Lock] = lock if lock is not None else Lock()
        self._value: LockableValue = value
