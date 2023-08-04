from __future__ import annotations

from typing import Any, Callable, TypeVar

from dualsense_controller.report.in_report.InReport import InReport
from dualsense_controller.state.read_state.enum import ReadStateName
from dualsense_controller.state.write_state.enum import WriteStateName

StateValueType = TypeVar('StateValueType')
MappedStateValueType = TypeVar('MappedStateValueType')
StateName = ReadStateName | WriteStateName | str

_StChCb0 = Callable[[], None]
_StChCb1 = Callable[[Any], None]
_StChCb2 = Callable[[Any, int | None], None]
_StChCb3 = Callable[[Any, Any, int | None], None]
_StChCb4 = Callable[[StateName, Any, Any, int | None], None]
StateChangeCallback = _StChCb0 | _StChCb1 | _StChCb2 | _StChCb3 | _StChCb4

Number = int | float
CompareResult = tuple[bool, StateValueType]
CompareFn = Callable[[StateValueType, StateValueType, ...], CompareResult]
StateValueFn = Callable[[InReport, ...], StateValueType]



