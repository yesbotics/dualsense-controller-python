from typing import Any

import hidapi

from dualsense_controller.common import ConnectionType, \
    InReportLength
from dualsense_controller.exceptions import InvalidConnectionTypeException
from dualsense_controller.reports import InReport, Usb01InReport, Bt31InReport, Bt01InReport, OutReport, Usb01OutReport, \
    Bt31OutReport, Bt01OutReport


class ControllerDevice:

    def __init__(
            self,
            device: hidapi.Device,
    ):
        super().__init__()

        self._hid_device = device
        self._connection_type: ConnectionType = ConnectionType.UNDEFINED
        self._report_length: InReportLength = InReportLength.DUMMY
        self._in_report_class = None
        self._out_report = None
        # self._out_report_class = None
        self._init()

    def _init(self):
        dummy_report: Any | None = self._hid_device.read(InReportLength.DUMMY)
        self._report_length: int = len(dummy_report)

        match self._report_length:
            case InReportLength.USB_01:
                self._connection_type = ConnectionType.USB_01
                self._in_report_class = Usb01InReport
                self._out_report = Usb01OutReport()
                # self._out_report_class = Usb01OutReport
            case InReportLength.BT_31:
                self._connection_type = ConnectionType.BT_31
                self._in_report_class = Bt31InReport
                self._out_report = Bt31OutReport()
                # self._out_report_class = Bt31OutReport
            case InReportLength.BT_01:
                self._connection_type = ConnectionType.BT_01
                self._in_report_class = Bt01InReport
                self._out_report = Bt01OutReport()
                # self._out_report_class = Bt01OutReport
            case _:
                raise InvalidConnectionTypeException

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    @property
    def out_report(self):
        return self._out_report

    def read(self) -> InReport:
        in_report_raw: bytes = self._hid_device.read(self._report_length)
        return self._in_report_class(in_report_raw)

    def write(self):
        data = self.out_report.to_bytes()
        # print(data)
        self._hid_device.write(data)

    def close(self):
        self._hid_device.close()
        self._hid_device = None
