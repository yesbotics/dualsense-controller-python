from enum import Enum


class InReportLength(int, Enum):
    DUMMY = 100
    USB_01 = 64
    BT_31 = 78
    BT_01 = 10
