from abc import ABC
from typing import Final, Any

from dualsense_controller import EventType, ConnectionType, StateName


class AbstractBaseEvent(ABC):
    def __init__(self, type_: EventType):
        self.type: Final[EventType] = type_


class ConnectionLookupEvent(AbstractBaseEvent):
    def __init__(self):
        super().__init__(EventType.CONNECTION_LOOKUP)


class ConnectionChangeEvent(AbstractBaseEvent):
    def __init__(self, connected: bool, connection_type: ConnectionType):
        super().__init__(EventType.CONNECTION_CHANGE)
        self.connected: Final[bool] = connected
        self.connection_type: Final[ConnectionType] = connection_type


class StateChangeEvent(AbstractBaseEvent):
    def __init__(self, name: StateName, old_value: Any, new_value: Any):
        super().__init__(EventType.STATE_CHANGE)
        self.name: StateName = name
        self.old_value: Final[Any] = old_value
        self.new_value: Final[Any] = new_value
