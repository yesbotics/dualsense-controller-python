import threading
from threading import Thread
from typing import Any, Final

import hidapi
import pyee as pyee

from dualsense_controller import ReadStates, State
from dualsense_controller.common import (
    VENDOR_ID,
    PRODUCT_ID,
    ConnectionType,
    StateName,
    ConnectionChangeCallback,
    EventType,
    ExceptionCallback,
    StateChangeCallback,
    AnyStateChangeCallback,
    ReportLength
)
from dualsense_controller.exceptions import (
    AlreadyInitializedException,
    NotInitializedYetException,
    NoDeviceDetectedException,
    InvalidDeviceIndexException,
    InvalidConnectionTypeException
)
from dualsense_controller.reports import InReport, Usb01InReport, Bt31InReport, Bt01InReport


# TODO: remove event listener
# TODO: access for states
# TODO: complex state packets (gyro value, pad x/y values (-1..1), orientation, touch finger, ...)
# TODO: Batt low warn option
# TODO: raw states
# TODO: impl set properties (rumble, triggerFX, lights, ...)
# TODO: only calculate values on subscribed event listeners


class DualSenseController:

    @staticmethod
    def enumerate_devices() -> list[hidapi.DeviceInfo]:
        return [device_info for device_info in hidapi.enumerate(vendor_id=VENDOR_ID)
                if device_info.vendor_id == VENDOR_ID and device_info.product_id == PRODUCT_ID]

    def __init__(
            self,
            device_index: int = 0,
            analog_threshold: int = 0,
            gyro_threshold: int = 0,
            accelerometer_threshold: int = 0,
    ):
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()
        self._read_states: Final[ReadStates] = ReadStates(
            analog_threshold=analog_threshold,
            gyroscope_threshold=gyro_threshold,
            accelerometer_threshold=accelerometer_threshold,
        )
        self._device_index: int = device_index
        self._hid_device: hidapi.Device | None = None
        self._stop_thread_event: threading.Event | None = None
        self._thread_controller_report: Thread | None = None
        self._connection_type: ConnectionType = ConnectionType.UNDEFINED
        self._initialized: bool = False

    @property
    def states(self) -> dict[StateName, State]:
        return self._read_states.states_dict

    def on_connection_change(self, callback: ConnectionChangeCallback):
        self._event_emitter.on(EventType.CONNECTION_CHANGE, callback)

    def on_exception(self, callback: ExceptionCallback):
        self._event_emitter.on(EventType.EXCEPTION, callback)

    def on_state_change(self, state_name: StateName, callback: StateChangeCallback):
        self._read_states.on_change(state_name, callback)

    def on_any_state_change(self, callback: AnyStateChangeCallback):
        self._read_states.on_change_any(callback)

    def init(self) -> None:
        if self._initialized:
            raise AlreadyInitializedException
        self._initialized = True
        self._stop_thread_event = threading.Event()
        self._open_device()

    def deinit(self) -> None:
        if not self._initialized:
            raise NotInitializedYetException
        self._stop_thread_event.set()
        self._close_device()
        self._stop_thread_event = None
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

    def _loop_controller_report(self) -> None:
        try:
            while not self._stop_thread_event.is_set():
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
                self._read_states.update(in_report, self._connection_type)
        except Exception as exception:
            self._event_emitter.emit(EventType.EXCEPTION, exception)
