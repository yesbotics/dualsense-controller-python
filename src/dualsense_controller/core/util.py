import inspect
import traceback
import warnings
from types import FrameType
from typing import Any

import numpy as np
from numpy import ndarray


def flag(bit: int) -> int:
    return 1 << bit


def format_exception(exception: Exception) -> str:
    traceback_list = traceback.format_exception(type(exception), exception, exception.__traceback__)
    formatted_traceback = ''.join(traceback_list)
    return formatted_traceback


def get_referencing_class() -> Any:
    current_frame: FrameType | None = inspect.currentframe()
    calling_frame: FrameType | None = current_frame.f_back
    return calling_frame.f_locals.get("self")


_Num = int | float


def _min_val(mapped_min_max_values: list[_Num]) -> _Num:
    return np.mean(np.abs(mapped_min_max_values))


def _max_val(mapped_min_max_values: list[_Num]) -> _Num:
    return np.max(np.abs(mapped_min_max_values))


def check_value_restrictions(
        name: str,
        mapped_min_max_values: list[_Num] = None,
        middle_deadzone: _Num = None,
        deadzone: _Num = None,
        threshold: _Num = None,
) -> None:
    if mapped_min_max_values is None:
        return
    if deadzone is not None or middle_deadzone is not None or threshold is not None:
        mapped_min_max_values = [v for v in mapped_min_max_values if v is not None]

    if len(mapped_min_max_values) >= 1 and deadzone is not None:
        if deadzone < 0:
            raise ValueError('Deadzone value must not be negative')
        max_map_val: _Num = _max_val(mapped_min_max_values)
        if deadzone >= max_map_val:
            msg: str = (
                "\nWarning:\n"
                f"Deadzone value for \"{name.split('.')[-1].lower()}\" is very big related to chosen mapping.\n"
                "Maybe changes are not reconized properly.\n"
                f"Deadzone for value should be lower than {max_map_val}. actual value is: {deadzone}"
            )
            warnings.warn(msg, UserWarning)

    if len(mapped_min_max_values) >= 1 and middle_deadzone is not None:
        if middle_deadzone < 0:
            raise ValueError('Deadzone value must not be negative')
        min_map_val: _Num = _min_val(mapped_min_max_values)
        if middle_deadzone >= min_map_val:
            msg: str = (
                "\nWarning:\n"
                f"Deadzone value for \"{name.split('.')[-1].lower()}\" is very big related to chosen mapping.\n"
                "Maybe changes are not reconized properly.\n"
                f"Deadzone for value should be lower than {min_map_val}. actual value is: {middle_deadzone}"
            )
            warnings.warn(msg, UserWarning)

    if len(mapped_min_max_values) >= 1 and threshold is not None:
        if threshold < 0:
            raise ValueError('Threshold value must not be negative')
        min_map_val: _Num = _min_val(mapped_min_max_values)
        if threshold >= min_map_val:
            msg: str = (
                "\nWarning:\n"
                f"Threshold value for \"{name.split('.')[-1].lower()}\" is very big related to chosen mapping.\n"
                "Maybe changes are not reconized.\n"
                f"Threshold for value should be lower than {min_map_val}. actual value is: {threshold}"
            )
            warnings.warn(msg, UserWarning)
