import threading
from threading import Thread
from typing import Any, Final, TypedDict

import hid
import hidapi
import pyee

from .typedef import ExceptionCallback
from .enum import ConnectionType, EventType

from dualsense_controller.exceptions import (
    InvalidConnectionTypeException,
    NoDeviceDetectedException,
    InvalidDeviceIndexException
)
from dualsense_controller.report import (
    InReport,
    Usb01InReport,
    Bt31InReport,
    Bt01InReport,
    OutReport,
    Usb01OutReport,
    Bt31OutReport,
    Bt01OutReport,
    InReportCallback, InReportLength
)


class HidDeviceInfo(TypedDict):
    path: bytes
    vendor_id: int
    product_id: int
    serial_number: str
    release_number: int
    manufacturer_string: str
    product_string: str
    usage_page: int
    usage: int
    interface_number: int


class HidControllerDevice:
    VENDOR_ID: Final[int] = 0x054c
    PRODUCT_ID: Final[int] = 0x0ce6

    @staticmethod
    def enumerate_devices() -> list[HidDeviceInfo]:
        return hid.enumerate(vendor_id=HidControllerDevice.VENDOR_ID, product_id=HidControllerDevice.PRODUCT_ID)

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    @property
    def device_index(self) -> int:
        return self._device_index

    @property
    def out_report(self):
        return self._out_report

    @property
    def opened(self) -> bool:
        return self._hid_device is not None

    def __init__(self, device_index: int = 0):
        self._device_index = device_index
        self._connection_type: ConnectionType = ConnectionType.UNDEFINED
        self._loop_thread: Thread | None = None
        self._stop_thread_event: threading.Event | None = None
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()

        hid_device_infos: list[HidDeviceInfo] = HidControllerDevice.enumerate_devices()
        num_hid_device_infos: int = len(hid_device_infos)
        if num_hid_device_infos < 1:
            raise NoDeviceDetectedException
        if num_hid_device_infos < self._device_index + 1:
            raise InvalidDeviceIndexException(self._device_index)
        device_info: HidDeviceInfo = hid_device_infos[self._device_index]
        self._serial_number = device_info['serial_number']
        # self._hid_device: hid.device = hid.device()
        self._hid_device: hidapi.Device | None = None

        self._in_report_length: InReportLength = InReportLength.DUMMY
        self._in_report: InReport | None = None
        self._out_report: OutReport | None = None

    def open(self):
        assert self._hid_device is None, "Device already opened"
        # self._hid_device.open(
        #     HidControllerDevice.VENDOR_ID,
        #     HidControllerDevice.PRODUCT_ID,
        #     self._serial_number
        # )
        self._hid_device: hidapi.Device = hidapi.Device(
            vendor_id=HidControllerDevice.VENDOR_ID,
            product_id=HidControllerDevice.PRODUCT_ID,
            serial_number=self._serial_number
        )
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

    def _detect(self) -> None:
        dummy_report: Any | None = self._hid_device.read(InReportLength.DUMMY)
        self._in_report_length: int = len(dummy_report)
        match self._in_report_length:
            case InReportLength.USB_01:
                self._connection_type = ConnectionType.USB_01
                self._in_report = Usb01InReport()
                self._out_report = Usb01OutReport()
            case InReportLength.BT_31:
                self._connection_type = ConnectionType.BT_31
                self._in_report = Bt31InReport()
                self._out_report = Bt31OutReport()
            case InReportLength.BT_01:
                self._connection_type = ConnectionType.BT_01
                self._in_report = Bt01InReport()
                self._out_report = Bt01OutReport()
            case _:
                raise InvalidConnectionTypeException

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
                self._in_report.update(raw_bytes)
                self._event_emitter.emit(EventType.IN_REPORT, self._in_report)
        except Exception as exception:
            self._event_emitter.emit(EventType.EXCEPTION, exception)
