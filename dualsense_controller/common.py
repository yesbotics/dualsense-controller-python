from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class DsBaseException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class AlreadyInitializedException(DsBaseException):
    def __init__(self):
        super().__init__('Already initialized')


class NotInitializedYetException(DsBaseException):
    def __init__(self):
        super().__init__('Not initialized yet')


class NoDeviceDetectedException(DsBaseException):
    def __init__(self):
        super().__init__('No DualSense device detected')


class InvalidDeviceIndexException(DsBaseException):
    def __init__(self, idx: int):
        super().__init__(f'Invalid DualSense device index given {idx}')


class EventType(Enum):
    CONNECTION_LOOKUP = 'CONNECTION_LOOKUP',
    CONNECTION_STATE_CHANGE = 'CONNECTION_STATE_CHANGE',
    VALUE_CHANGE = 'VALUE_CHANGE',


@dataclass(frozen=True, slots=True)
class Event:
    type: EventType
    data: Any
