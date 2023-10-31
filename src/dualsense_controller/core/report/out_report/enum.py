from enum import Enum


class OutReportLength(int, Enum):
    USB_01 = 48
    BT_31 = 78
    BT_01 = 10
