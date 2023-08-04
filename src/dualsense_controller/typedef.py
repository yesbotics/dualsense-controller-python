from typing import Callable

ExceptionCallback = Callable[[Exception], None]
SimpleCallback = Callable[[], None]
BatteryLowCallback = Callable[[float], None]
