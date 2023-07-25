from typing import Callable

from .enum import ConnectionType

ExceptionCallback = Callable[[Exception], None]
SimpleCallback = Callable[[], None]
BatteryLowCallback = Callable[[float], None]
ConnectionChangeCallback = Callable[[bool, ConnectionType], None]
