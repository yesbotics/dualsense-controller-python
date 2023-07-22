import threading
from threading import Thread
from time import sleep
from typing import Any

import hidapi
import pyee as pyee

from dualsense_controller import AlreadyInitializedException, NotInitializedYetException, \
    ConnectionType, InvalidConnectionTypeException, States, CONNECTION_LOOKUP_INTERVAL, PRODUCT_ID, \
    VENDOR_ID, StateName, ReportLength, Usb01InReport, \
    InReport, Bt31InReport, Bt01InReport, EventType, StateChangeCallback, ConnectionChangeCallback, SimpleCallback, \
    AnyStateChangeCallback
from dualsense_controller import NoDeviceDetectedException, InvalidDeviceIndexException


# TODO: fix crash on deinit when no connection lookup
# TODO: complex state packets
# TODO: Batt low warn option
# TODO: orientation calc
# TODO: raw states
# TODO: listen state collection event (all states)
# TODO: impl set properties (rumble, triggerFX)


class DualSenseController:

    @staticmethod
    def enumerate_devices() -> list[hidapi.DeviceInfo]:
        return [device_info for device_info in hidapi.enumerate(vendor_id=VENDOR_ID)
                if device_info.vendor_id == VENDOR_ID and device_info.product_id == PRODUCT_ID]

    def __init__(
            self,
            device_index: int = 0,
            enable_connection_lookup: bool = False,
            connection_lookup_interval: float = CONNECTION_LOOKUP_INTERVAL,
            analog_threshold: int = 0,
            gyro_threshold: int = 0,
            accelerometer_threshold: int = 0,
    ):
        self._device_index: int = device_index
        self._enable_connection_lookup: bool = enable_connection_lookup
        self._connection_lookup_interval: float = connection_lookup_interval
        self._hid_device: hidapi.Device | None = None
        self._event_emitter: pyee.EventEmitter = pyee.EventEmitter()
        self._run_thread: bool = False
        self._thread_lookup_connection: Thread | None = None
        self._thread_controller_report: Thread | None = None
        self._initialized: bool = False
        self._connection_type: ConnectionType = ConnectionType.UNDEFINED
        self._states: States = States(
            analog_threshold=analog_threshold,
            gyroscope_threshold=gyro_threshold,
            accelerometer_threshold=accelerometer_threshold,
        )

    def on_connection_lookup(self, callback: SimpleCallback):
        self._event_emitter.on(EventType.CONNECTION_LOOKUP, callback)

    def on_connection_change(self, callback: ConnectionChangeCallback):
        self._event_emitter.on(EventType.CONNECTION_CHANGE, callback)

    def on_state_change(self, state_name: StateName, callback: StateChangeCallback):
        self._states.on_change(state_name, callback)

    def on_any_state_change(self, callback: AnyStateChangeCallback):
        self._states.on_change_any(callback)

    def init(self) -> None:
        if self._initialized:
            raise AlreadyInitializedException
        self._initialized = True
        self._run_thread = True
        if self._enable_connection_lookup:
            self._thread_lookup_connection = threading.Thread(
                target=self._loop_lookup_connection,
                daemon=True,
            )
            self._thread_lookup_connection.start()
        else:
            self._open_device()

    def deinit(self) -> None:
        if not self._initialized:
            raise NotInitializedYetException
        self._run_thread = False
        if self._enable_connection_lookup:
            self._thread_lookup_connection.join()
            self._thread_lookup_connection = None
        else:
            self._close_device()
        self._initialized = False

    def _open_device(self) -> None:
        devices: list[hidapi.DeviceInfo] = DualSenseController.enumerate_devices()
        num_devices: int = len(devices)
        if num_devices < 1:
            raise NoDeviceDetectedException
        if num_devices < self._device_index + 1:
            raise InvalidDeviceIndexException(self._device_index)
        device_info: hidapi.DeviceInfo = devices[self._device_index]
        self._hid_device = hidapi.Device(vendor_id=device_info.vendor_id, product_id=device_info.product_id)
        self._connection_type = self._detect_connection_type()
        self._event_emitter.emit(EventType.CONNECTION_CHANGE, True, self._connection_type)
        self._thread_controller_report = threading.Thread(
            target=self._loop_controller_report,
            daemon=True,
        )
        self._thread_controller_report.start()

    def _close_device(self) -> None:
        self._thread_controller_report.join()
        self._thread_controller_report = None
        self._hid_device.close()
        self._hid_device = None
        self._event_emitter.emit(EventType.CONNECTION_CHANGE, False, self._connection_type)
        self._connection_type = None

    def _detect_connection_type(self) -> ConnectionType:
        dummy_report: Any | None = self._hid_device.read(ReportLength.DUMMY)
        input_report_length: int = len(dummy_report)
        match input_report_length:
            case ReportLength.USB_01:
                return ConnectionType.USB_01
            case ReportLength.BT_31:
                return ConnectionType.BT_31
            case ReportLength.BT_01:
                return ConnectionType.BT_01
        raise InvalidConnectionTypeException

    def _loop_lookup_connection(self) -> None:
        while self._run_thread:
            if self._hid_device is None:
                self._event_emitter.emit(EventType.CONNECTION_LOOKUP)
                try:
                    self._open_device()
                except NoDeviceDetectedException:
                    pass
            sleep(self._connection_lookup_interval)
        if self._hid_device:
            self._close_device()

    def _loop_controller_report(self) -> None:
        while self._run_thread:
            in_report_raw: bytes
            in_report: InReport
            match self._connection_type:
                case ConnectionType.USB_01:
                    in_report_raw = self._hid_device.read(ReportLength.USB_01)
                    in_report = Usb01InReport(in_report_raw)
                case ConnectionType.BT_31:
                    in_report_raw = self._hid_device.read(ReportLength.BT_31)
                    in_report = Bt31InReport(in_report_raw)
                case ConnectionType.BT_01:
                    in_report_raw = self._hid_device.read(ReportLength.BT_01)
                    in_report = Bt01InReport(in_report_raw)
                case _:
                    raise InvalidConnectionTypeException
            self._states.update(in_report, self._connection_type)
