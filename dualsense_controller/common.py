from enum import Enum
from typing import Any, Final


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


class InvalidReportIdException(DsBaseException):
    def __init__(self):
        super().__init__(f'Invalid report id')


class EventType(Enum):
    CONNECTION_LOOKUP = 'CONNECTION_LOOKUP',
    CONNECTION_STATE_CHANGE = 'CONNECTION_STATE_CHANGE',
    VALUE_CHANGE = 'VALUE_CHANGE',


class Event:

    def __init__(self, type_: EventType, *data: Any):
        self.type: Final[EventType] = type_
        self.data: Final[tuple[Any, ...]] = data


class ConnectionType(Enum):
    UNDEFINED = 'UNDEFINED',
    USB_01 = 'USB',
    BT_01 = 'BT',
    BT_31 = 'BT',
