import threading
from threading import Thread
from typing import Any, Final

import pyee

from dualsense_controller.core.hidapi import Device, DeviceInfo, enumerate
from dualsense_controller.core.enum import ConnectionType, EventType
from dualsense_controller.core.exception import InvalidDeviceIndexException, InvalidInReportLengthException, \
    NoDeviceDetectedException
from dualsense_controller.core.report.ReportWrap import ReportWrap
from dualsense_controller.core.report.in_report.Bt01InReport import Bt01InReport
from dualsense_controller.core.report.in_report.Bt31InReport import Bt31InReport
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.report.in_report.Usb01InReport import Usb01InReport
from dualsense_controller.core.report.in_report.enum import InReportLength
from dualsense_controller.core.report.in_report.typedef import InReportCallback
from dualsense_controller.core.report.out_report.Bt31OutReport import Bt01OutReport, Bt31OutReport
from dualsense_controller.core.report.out_report.OutReport import OutReport
from dualsense_controller.core.report.out_report.Usb01OutReport import Usb01OutReport
from dualsense_controller.core.typedef import ExceptionCallback


class HidControllerDevice:
    VENDOR_ID: Final[int] = 0x054c
    PRODUCT_ID: Final[int] = 0x0ce6

    @staticmethod
    def enumerate_devices() -> list[DeviceInfo]:
        return enumerate(vendor_id=HidControllerDevice.VENDOR_ID, product_id=HidControllerDevice.PRODUCT_ID)

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    @property
    def out_report(self) -> OutReport:
        return self._out_report_wrap.report

    @property
    def is_opened(self) -> bool:
        return self._hid_device is not None

    def __init__(self, device_index_or_device_info: int | DeviceInfo = 0):
        self._connection_type: ConnectionType = ConnectionType.UNDEFINED
        self._loop_thread: Thread | None = None
        self._stop_thread_event: threading.Event | None = None
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()

        device_info: DeviceInfo
        if isinstance(device_index_or_device_info, int):
            device_index: int = device_index_or_device_info
            hid_device_infos: list[DeviceInfo] = HidControllerDevice.enumerate_devices()
            num_hid_device_infos: int = len(hid_device_infos)
            if num_hid_device_infos < 1:
                raise NoDeviceDetectedException
            if num_hid_device_infos < device_index + 1:
                raise InvalidDeviceIndexException(device_index)
            device_info = hid_device_infos[device_index]
        else:
            device_info = device_index_or_device_info
        self._serial_number = device_info.serial_number
        self._hid_device: Device | None = None

        self._in_report_length: InReportLength = InReportLength.DUMMY
        self._in_report_wrap: Final[ReportWrap] = ReportWrap()
        self._out_report_wrap: Final[ReportWrap] = ReportWrap()

    def open(self):
        assert self._hid_device is None, "Device already opened"
        self._hid_device: Device = self._create()
        self._detect()
        self._start_loop_thread()

    def close(self) -> None:
        assert self._hid_device is not None, "Device already opened"
        self._stop_loop_thread()
        self._hid_device.close()
        self._hid_device = None

    def write(self) -> None:
        data = self.out_report.to_bytes()
        # print(data)
        print(data.hex(' '), end='\n')
        self._hid_device.write(data)

    def on_exception(self, callback: ExceptionCallback) -> None:
        self._event_emitter.on(EventType.EXCEPTION, callback)

    def on_in_report(self, callback: InReportCallback) -> None:
        self._event_emitter.on(EventType.IN_REPORT, callback)

    def _create(self) -> Device:
        return Device(
            vendor_id=HidControllerDevice.VENDOR_ID,
            product_id=HidControllerDevice.PRODUCT_ID,
            serial_number=self._serial_number
        )

    def _detect(self) -> None:
        dummy_report_bytes: bytes = self._hid_device.read(InReportLength.DUMMY)
        self._in_report_length: int = len(dummy_report_bytes)
        match self._in_report_length:
            case InReportLength.USB_01:
                self._connection_type = ConnectionType.USB_01
                self._in_report_wrap.report = Usb01InReport()
                self._out_report_wrap.report = Usb01OutReport()
            case InReportLength.BT_31:
                self._connection_type = ConnectionType.BT_31
                self._in_report_wrap.report = Bt31InReport()
                self._out_report_wrap.report = Bt31OutReport()
            case InReportLength.BT_01:
                self._connection_type = ConnectionType.BT_01
                self._in_report_wrap.report = Bt01InReport()
                self._out_report_wrap.report = Bt01OutReport()
            case _:
                raise InvalidInReportLengthException

    def _start_loop_thread(self) -> None:
        self._stop_thread_event = threading.Event()
        self._loop_thread = Thread(
            target=self._loop,
            daemon=True,
        )
        self._loop_thread.start()

    def _stop_loop_thread(self) -> None:
        self._stop_thread_event.set()
        self._loop_thread.join()
        self._loop_thread = None
        self._stop_thread_event = None

    def _loop(self) -> None:
        try:
            while not self._stop_thread_event.is_set():
                raw_bytes: bytes = self._hid_device.read(self._in_report_length)
                self._in_report_wrap.report.update(raw_bytes)
                self._event_emitter.emit(EventType.IN_REPORT, self._in_report_wrap.report)
        except Exception as exception:
            self._event_emitter.emit(EventType.EXCEPTION, exception)
