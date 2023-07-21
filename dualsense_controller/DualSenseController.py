import threading
from threading import Thread
from time import sleep
from typing import Callable, Any

import hidapi
import pyee as pyee

from dualsense_controller import EventType, AbstractBaseEvent, AlreadyInitializedException, NotInitializedYetException, \
    ConnectionType, InvalidReportIdException, States, REPORT_USB_LEN, REPORT_DUMMY_LEN, REPORT_BT_LEN, \
    CONNECTION_LOOKUP_INTERVAL, PRODUCT_ID, VENDOR_ID, StateName, ConnectionLookupEvent, ConnectionChangeEvent, \
    StateChangeEvent
from dualsense_controller import NoDeviceDetectedException, InvalidDeviceIndexException


# TODO: Batt low warn option
# TODO: orientation calc
# TODO: raw states
# TODO: listen state collection event (all states)
# TODO: complex state packets
# TODO: impl set properties (rumble, triggerFX)
# TODO: listen for all or for specific changes only?


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
        self._states.on(States.EVENT_CHANGE, self._on_state_change)

    def add_event_listener(self, event_type: EventType, callback: Callable[[AbstractBaseEvent], None]) -> None:
        self._event_emitter.on(event_type.name, callback)

    def remove_event_listener(self, event_type: EventType, callback: Callable[[AbstractBaseEvent], None]) -> None:
        self._event_emitter.remove_listener(event_type.name, callback)

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
        self._event_emitter.emit(
            EventType.CONNECTION_CHANGE.name,
            ConnectionChangeEvent(connected=True, connection_type=self._connection_type)
        )
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
        self._event_emitter.emit(
            EventType.CONNECTION_CHANGE.name,
            ConnectionChangeEvent(connected=False, connection_type=self._connection_type)
        )
        self._connection_type = None

    def _detect_connection_type(self) -> ConnectionType:
        dummy_report: Any | None = self._hid_device.read(REPORT_DUMMY_LEN)
        input_report_length = len(dummy_report)
        if input_report_length == REPORT_BT_LEN:
            report_id: int = list(dummy_report)[0]
            if report_id == 0x31:
                return ConnectionType.BT_31
            elif report_id == 0x01:
                return ConnectionType.BT_01
            else:
                raise InvalidReportIdException
        elif input_report_length == REPORT_USB_LEN:
            return ConnectionType.USB_01
        return ConnectionType.UNDEFINED

    def _loop_lookup_connection(self) -> None:
        while self._run_thread:
            if self._hid_device is None:
                self._event_emitter.emit(
                    EventType.CONNECTION_LOOKUP.name,
                    ConnectionLookupEvent()
                )
                try:
                    self._open_device()
                except NoDeviceDetectedException:
                    pass
            sleep(self._connection_lookup_interval)
        if self._hid_device:
            self._close_device()

    def _loop_controller_report(self) -> None:
        while self._run_thread:
            match self._connection_type:
                case ConnectionType.BT_01:
                    self._handle_BT01()
                case ConnectionType.BT_31:
                    self._handle_BT_31()
                case ConnectionType.USB_01:
                    self._handle_USB_01()
            # sleep(1)

    def _handle_BT01(self) -> None:
        report: bytes = self._hid_device.read(REPORT_BT_LEN)
        raise NotImplementedError

    def _handle_BT_31(self) -> None:
        report: bytes = self._hid_device.read(REPORT_BT_LEN)
        raise NotImplementedError

    def _handle_USB_01(self) -> None:
        report: bytes = self._hid_device.read(REPORT_USB_LEN)
        self._states.update(report=report[1:])

    def _on_state_change(self, name: StateName, old_value: Any, new_value: Any) -> None:
        self._event_emitter.emit(
            EventType.STATE_CHANGE.name,
            StateChangeEvent(name=name, old_value=old_value, new_value=new_value)
        )
