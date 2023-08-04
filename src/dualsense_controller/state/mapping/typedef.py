from typing import Any, Callable

from dualsense_controller.state.typedef import Number

FromToTuple = tuple[Number, Number, Number, Number]
MapFn = Callable[[Any], Any]
