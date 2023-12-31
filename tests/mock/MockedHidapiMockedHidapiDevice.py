from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.report.in_report.Bt01InReport import Bt01InReport
from dualsense_controller.core.report.in_report.Bt31InReport import Bt31InReport
from dualsense_controller.core.report.in_report.Usb01InReport import Usb01InReport
from dualsense_controller.core.state.read_state.ValueCalc import ValueCalc
from dualsense_controller.core.state.read_state.value_type import JoyStick


class _BaseMockedHidapiDevice:

    def __init__(self, conn_type: ConnectionType = ConnectionType.USB_01):
        self._in_report: InReport | None = None
        match conn_type:
            case ConnectionType.USB_01:
                self._in_report = Usb01InReport(raw_bytes=bytearray(
                    b'\x01\x80\x80\x82\x83\x00\x00\x9c\x08\x00\x00\x00\x1c\x8f\xcc '
                    b'\x03\x00\xfc\xff\x03\x00\xb0\xff\xeb\x1e\x82\x06\xbf@\xb1\t\x02'
                    b'\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\t\x00\x00\x00\x00\x00\x03Z'
                    b'\xb1\t)\x08\x00\xdd\xedU\xeb%{\x97\xc3'
                ))
            case ConnectionType.BT_31:
                self._in_report = Bt31InReport(raw_bytes=bytearray(
                    b'1\x01\x80\x81\x82\x83\x00\x00\x01\x08\x00\x00\x00\xae\xab\x8b\xf2'
                    b'\x02\x00\xfc\xff\x02\x00\xdc\xff\xda\x1e\x9e\x06\xc7\xb5\xe4\x00\x08'
                    b'\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\t\x00\x00\x00\x00\x00\xc3\xc9\xe4'
                    b'\x00\t\x00\x00\xaf\xc5\x1af\xc2\xf3\x16\xbd\x00\x00\x00\x00\x00\x00\x00\x00\x00B\xd7\xd8\r'
                ))
            case ConnectionType.BT_01:
                self._in_report = Bt01InReport(raw_bytes=bytearray(
                    b'\x01\x80\x80\x82\x83\x00\x00\x9c\x08\x00'
                ))

    def write(self, data: bytes):
        pass

    def read(self, _: int, **kwargs) -> bytes:
        return self._in_report.raw_bytes

    def close(self):
        pass


class MockedHidapiMockedHidapiDevice(_BaseMockedHidapiDevice):

    def set_left_stick_raw(self, value: JoyStick):
        ValueCalc.set_left_stick(self._in_report, value)

    def set_left_stick_x_raw(self, value: int):
        ValueCalc.set_left_stick_x(self._in_report, value)

    def set_left_stick_y_raw(self, value: int):
        ValueCalc.set_left_stick_y(self._in_report, value)

    def set_right_stick_raw(self, value: JoyStick):
        ValueCalc.set_right_stick(self._in_report, value)

    def set_right_stick_x_raw(self, value: int):
        ValueCalc.set_right_stick_x(self._in_report, value)

    def set_right_stick_y_raw(self, value: int):
        ValueCalc.set_right_stick_y(self._in_report, value)

    def set_left_trigger_raw(self, value: int):
        ValueCalc.set_left_trigger(self._in_report, value)

    def set_right_trigger_raw(self, value: int):
        ValueCalc.set_right_trigger(self._in_report, value)

    def set_btn_square(self, value: bool):
        ValueCalc.set_btn_square(self._in_report, value)

    def set_btn_cross(self, value: bool):
        ValueCalc.set_btn_cross(self._in_report, value)
