from typing import Callable

ExceptionCallback = Callable[[Exception], None]
EmptyCallback = Callable[[], None]
BatteryLowCallback = Callable[[float], None]
