from enum import Enum


class EventType(str, Enum):
    EXCEPTION = 'EXCEPTION'
    CONNECTION_CHANGE = 'CONNECTION_CHANGE'
    IN_REPORT = 'IN_REPORT'


class ConnectionType(Enum):
    UNDEFINED = 'UNDEFINED',
    USB_01 = 'USB',
    BT_31 = 'BT',
    BT_01 = 'BT'
