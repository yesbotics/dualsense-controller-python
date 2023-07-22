from typing import Any

import hidapi

from dualsense_controller.common import ConnectionType, \
    ReportLength
from dualsense_controller.exceptions import InvalidConnectionTypeException
from dualsense_controller.reports import InReport, Usb01InReport, Bt31InReport, Bt01InReport


class ControllerDevice:

    def __init__(
            self,
            device: hidapi.Device,
    ):
        super().__init__()

        self._hid_device = device
        self._connection_type: ConnectionType = ConnectionType.UNDEFINED
        self._report_length: ReportLength = ReportLength.DUMMY
        self._report_class = None
        self._init()

    def _init(self):
        dummy_report: Any | None = self._hid_device.read(ReportLength.DUMMY)
        self._report_length: int = len(dummy_report)

        match self._report_length:
            case ReportLength.USB_01:
                self._connection_type = ConnectionType.USB_01
                self._report_class = Usb01InReport
            case ReportLength.BT_31:
                self._connection_type = ConnectionType.BT_31
                self._report_class = Bt31InReport
            case ReportLength.BT_01:
                self._connection_type = ConnectionType.BT_01
                self._report_class = Bt01InReport
            case _:
                raise InvalidConnectionTypeException

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    def read(self) -> InReport:
        in_report_raw: bytes = self._hid_device.read(self._report_length)
        return self._report_class(in_report_raw)

    def close(self):
        self._hid_device.close()
        self._hid_device = None
