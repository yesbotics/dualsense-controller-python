from dataclasses import dataclass
from enum import Enum


@dataclass
class DeviceInfoMock:
    path: str = '/dev/hidraw0'
    vendor_id: int = 0x054c
    product_id: int = 0x0ce6
    serial_number: str = 'a0:ab:51:a2:8c:1b'
    release_number: int = 256
    manufacturer_string: str = 'Sony Interactive Entertainment'
    product_string: str = 'Wireless Controller'
    usage_page: int = 1
    usage: int = 5
    interface_number: int = 3


class ConnTypeMock(Enum):
    BT_01 = 0
    BT_31 = 1
    USB_01 = 2



