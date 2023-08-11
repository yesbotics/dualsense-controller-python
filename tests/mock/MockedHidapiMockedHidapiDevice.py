from tests.mock.common import ConnTypeMock
from tests.mock.InRep import InRep
from tests.mock.InRepBt01 import InRepBt01
from tests.mock.InRepBt31 import InRepBt31
from tests.mock.InRepUsb01 import InRepUsb01


class _BaseMockedHidapiDevice:

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


class MockedHidapiMockedHidapiDevice(_BaseMockedHidapiDevice):

    def set_left_stick_x_raw(self, value: int):
        self._in_rep.set_axes_0(value)

    def set_left_stick_y_raw(self, value: int):
        self._in_rep.set_axes_1(value)

    def set_right_stick_x_raw(self, value: int):
        self._in_rep.set_axes_2(value)

    def set_right_stick_y_raw(self, value: int):
        self._in_rep.set_axes_3(value)

    def set_left_trigger_raw(self, value: int):
        self._in_rep.set_axes_4(value)

    def set_right_trigger_raw(self, value: int):
        self._in_rep.set_axes_5(value)

    # def set_btn_square(self, value: bool):
    #
    #     if value:
    #         return value | 0x10  # Set the 5th bit to 1
    #     else:
    #         return value & 0xEF  # Set the 5th bit to 0
    #     self._in_rep.get_buttons_0()

    # def set_btn_cross(self, value: bool):
    #     self._in_rep.set_buttons_0()
    #     return bool(in_report.buttons_0 & 0x20)