from __future__ import annotations

from typing import Any, Callable, TypeVar

from dualsense_controller.core.report.in_report import InReport
from dualsense_controller.core.state.enum import MixedStateName
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.write_state.enum import WriteStateName

StateValue = TypeVar('StateValue')
MappedStateValue = TypeVar('MappedStateValue')
StateName = ReadStateName | WriteStateName | MixedStateName | str

_StChCb0 = Callable[[], None]
_StChCb1 = Callable[[Any], None]
_StChCb2 = Callable[[Any, int | None], None]
_StChCb3 = Callable[[Any, Any, int | None], None]
_StChCb4 = Callable[[StateName, Any, Any, int | None], None]
StateChangeCallback = _StChCb0 | _StChCb1 | _StChCb2 | _StChCb3 | _StChCb4

Number = int | float
CompareResult = tuple[bool, StateValue]
_WrappedCompareFn = Callable[[StateValue, StateValue, ...], CompareResult]
_CompareFn = Callable[[StateValue, StateValue], CompareResult]
CompareFn = _WrappedCompareFn | _CompareFn
StateValueFn = Callable[[InReport, ...], StateValue]
