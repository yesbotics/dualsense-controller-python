from typing import Callable, TypeVar

from dualsense_controller.core.UpdateBenchmark import UpdateBenchmarkResult

ExceptionCallback = Callable[[Exception], None]
UpdateBenchmarkCallback = Callable[[UpdateBenchmarkResult], None]
EmptyCallback = Callable[[], None]
BatteryLowCallback = Callable[[float], None]
LockableValue = TypeVar('LockableValue')
