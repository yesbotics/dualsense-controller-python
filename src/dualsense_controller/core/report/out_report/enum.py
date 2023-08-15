from enum import Enum


class OutReportId(int, Enum):
    USB_01 = 0x02
    BT_31 = 0x31
    BT_01 = 0x31  # ??


class OutReportLength(int, Enum):
    USB_01 = 48
    BT_31 = 78
    BT_01 = 10
    # USB_01 = 47
    # BT_31 = 77
    # BT_01 = 77  # ??
