from dataclasses import dataclass
from enum import Enum

from tests.mock.in_rep.InRep import InRep
from tests.mock.in_rep.InRepBt01 import InRepBt01
from tests.mock.in_rep.InRepBt31 import InRepBt31
from tests.mock.in_rep.InRepUsb01 import InRepUsb01


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


class _BaseDeviceMock:

    def __init__(self, conn_type: ConnTypeMock = ConnTypeMock.USB_01):
        self._in_rep: InRep | None = None
        match conn_type:
            case ConnTypeMock.USB_01:
                self._in_rep = InRepUsb01()
            case ConnTypeMock.BT_31:
                self._in_rep = InRepBt31()
            case ConnTypeMock.BT_01:
                self._in_rep = InRepBt01()

    def write(self, data: bytes):
        pass

    def read(self, _: int, **kwargs) -> bytes:
        return self._in_rep.raw_bytes

    def close(self):
        pass


class MockedHidapiDevice(_BaseDeviceMock):

    def set_left_stick_x_byte(self, value: int):
        self._in_rep.set_axes_0(value)

    def set_left_stick_y_byte(self, value: int):
        self._in_rep.set_axes_1(value)
