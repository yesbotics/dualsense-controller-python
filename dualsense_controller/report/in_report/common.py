from enum import Enum
from typing import Callable

from .InReport import InReport

InReportCallback = Callable[[InReport], None]


class InReportLength(int, Enum):
    DUMMY = 100
    USB_01 = 64
    BT_31 = 78
    BT_01 = 10
