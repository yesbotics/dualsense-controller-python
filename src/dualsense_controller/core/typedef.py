from typing import Callable, TypeVar, Generic

ExceptionCallback = Callable[[Exception], None]
EmptyCallback = Callable[[], None]
BatteryLowCallback = Callable[[float], None]
LockableValue = TypeVar('LockableValue')
