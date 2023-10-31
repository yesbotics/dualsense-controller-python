from enum import Enum


class EventType(str, Enum):
    UPDATE_BENCHMARK = "UPDATE_BENCHMARK"
    EXCEPTION = 'EXCEPTION'
    CONNECTION_CHANGE = 'CONNECTION_CHANGE'
    IN_REPORT = 'IN_REPORT'


class ConnectionType(Enum):
    UNDEFINED = r"¯\_(ツ)_/¯",
    USB_01 = "USB",
    BT_31 = "Bluetooth",
    BT_01 = "Bluetooth (minimum features)"

    def __str__(self) -> str:
        return str(self.value[0]) if isinstance(self.value, tuple) else self.value
