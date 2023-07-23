import threading
from threading import Thread
from typing import Final

import hidapi
import pyee as pyee

from dualsense_controller import ReadStates, WriteStates, ControllerDevice
from dualsense_controller.common import (
    VENDOR_ID,
    PRODUCT_ID,
    ReadStateName,
    ConnectionChangeCallback,
    EventType,
    ExceptionCallback,
    StateChangeCallback,
    AnyStateChangeCallback,
    WriteStateName, BatteryLowCallback
)
from dualsense_controller.exceptions import (
    AlreadyInitializedException,
    NotInitializedYetException,
    NoDeviceDetectedException,
    InvalidDeviceIndexException
)


# TODO: remove event listener
# TODO: only calculate values on subscribed event listeners
# TODO: complex state packets (gyro value, pad x/y values (-1..1), orientation, touch finger, ...)
# TODO: fix batt level
# TODO: impl set properties (rumble, triggerFX, li50ghts, ...)


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
        self._write_states: Final[WriteStates] = WriteStates()
        self._device_index: int = device_index
        self._stop_thread_event: threading.Event | None = None
        self._thread_controller_report: Thread | None = None
        self._controller_device: ControllerDevice | None = None
        self._initialized: bool = False

    @property
    def states(self) -> ReadStates:
        return self._read_states

    def on_battery_low(self, level_percentage: float, callback: BatteryLowCallback):
        battery_low_level_percentage: float = level_percentage

        def check(_: float | None, batt_level_percentage: float) -> None:
            if batt_level_percentage <= battery_low_level_percentage:
                callback(batt_level_percentage)

        self.states.battery_level_percent.on_change(check)

    def on_connection_change(self, callback: ConnectionChangeCallback):
        self._event_emitter.on(EventType.CONNECTION_CHANGE, callback)

    def on_exception(self, callback: ExceptionCallback):
        self._event_emitter.on(EventType.EXCEPTION, callback)

    def on_state_change(self, state_name: ReadStateName | AnyStateChangeCallback, callback: StateChangeCallback = None):
        self._read_states.on_change(state_name, callback)

    def on_any_state_change(self, callback: AnyStateChangeCallback):
        self._read_states.on_any_change(callback)

    def set_state(self, state_name: WriteStateName, value):
        self._write_states.set_value(state_name, value)

    def set_motor_left(self, amount: int):
        self._write_states.set_value(WriteStateName.MOTOR_LEFT, amount)

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
        hid_device = hidapi.Device(vendor_id=device_info.vendor_id, product_id=device_info.product_id)
        self._controller_device = ControllerDevice(hid_device)
        self._event_emitter.emit(EventType.CONNECTION_CHANGE, True, self._controller_device.connection_type)
        self._thread_controller_report = threading.Thread(
            target=self._loop_controller_report,
            daemon=True,
        )
        self._thread_controller_report.start()

    def _close_device(self) -> None:
        self._thread_controller_report.join()
        self._thread_controller_report = None
        connection_type = self._controller_device.connection_type
        self._controller_device.close()
        self._controller_device = None
        self._event_emitter.emit(EventType.CONNECTION_CHANGE, False, connection_type)

    def _loop_controller_report(self) -> None:
        try:
            while not self._stop_thread_event.is_set():
                in_report = self._controller_device.read()
                self._read_states.update(in_report, self._controller_device.connection_type)

                if self._write_states.changed:
                    # print(f'Sending report.')
                    self._write_states.update_out_report(self._controller_device.out_report)
                    self._write_states.set_unchanged()
                    self._controller_device.write()

        except Exception as exception:
            self._event_emitter.emit(EventType.EXCEPTION, exception)
