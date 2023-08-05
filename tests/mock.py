from dataclasses import dataclass
from enum import Enum
from typing import Final, Literal


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
    BT_01: Final[bytes] = bytearray()
    BT_31: Final[bytes] = (
        b'1\x01\x80\x81\x82\x83\x00\x00\x01\x08\x00\x00\x00\xae\xab\x8b\xf2'
        b'\x02\x00\xfc\xff\x02\x00\xdc\xff\xda\x1e\x9e\x06\xc7\xb5\xe4\x00\x08'
        b'\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\t\x00\x00\x00\x00\x00\xc3\xc9\xe4'
        b'\x00\t\x00\x00\xaf\xc5\x1af\xc2\xf3\x16\xbd\x00\x00\x00\x00\x00\x00\x00\x00\x00B\xd7\xd8\r'
    )
    USB_01: Final[bytes] = (
        b'\x01\x80\x80\x82\x83\x00\x00\x9c\x08\x00\x00\x00\x1c\x8f\xcc '
        b'\x03\x00\xfc\xff\x03\x00\xb0\xff\xeb\x1e\x82\x06\xbf@\xb1\t\x02'
        b'\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\t\x00\x00\x00\x00\x00\x03Z'
        b'\xb1\t)\x08\x00\xdd\xedU\xeb%{\x97\xc3'
    )


class DeviceMock:

    def __init__(self, conn_type: ConnTypeMock = ConnTypeMock.USB_01):
        self._conn_type: ConnTypeMock = conn_type

    def write(self, data: bytes):
        pass

    def read(self, _: int, **kwargs) -> bytes:
        return self._conn_type.value

    def close(self):
        pass
