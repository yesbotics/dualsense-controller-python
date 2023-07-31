import inspect
import traceback
from types import FrameType
from typing import Any


def flag(bit: int) -> int:
    return 1 << bit


def clamp(value: int, val_min: int, val_max: int) -> int:
    return min(val_max, max(val_min, value))


def clamp_byte(value: int) -> int:
    return min(255, max(0, value))


def format_exception(exception: Exception) -> str:
    traceback_list = traceback.format_exception(type(exception), exception, exception.__traceback__)
    formatted_traceback = ''.join(traceback_list)
    return formatted_traceback


def get_referencing_class() -> Any:
    current_frame: FrameType | None = inspect.currentframe()
    calling_frame: FrameType | None = current_frame.f_back
    return calling_frame.f_locals.get("self")
