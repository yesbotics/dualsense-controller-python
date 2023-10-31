from typing import Callable, TypeVar

from dualsense_controller.core.Benchmarker import Benchmark

ExceptionCallback = Callable[[Exception], None]
UpdateBenchmarkCallback = Callable[[Benchmark], None]
EmptyCallback = Callable[[], None]
BatteryLowCallback = Callable[[float], None]
LockableValue = TypeVar('LockableValue')
