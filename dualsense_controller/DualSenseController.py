from typing import Final

from dualsense_controller import HidControllerDevice
from dualsense_controller.report import InReport
from dualsense_controller.state import (
    Connection, Number, ReadStateName, ReadStates,
    State, StateChangeCb, StateValueMapping, WriteStateName, WriteStates
)
from dualsense_controller.util import format_exception
from .core import hidapi
from .enums import EventType
from .typedef import BatteryLowCallback, ExceptionCallback


class DualSenseController:

    @staticmethod
    def enumerate_devices() -> list[hidapi.DeviceInfo]:
        return HidControllerDevice.enumerate_devices()

    def __init__(
            self,
            # ##### BASE  #####
            device_index_or_device_info: int | hidapi.DeviceInfo = 0,
            # ##### FEELING  #####
            left_joystick_deadzone: Number = 0,
            right_joystick_deadzone: Number = 0,
            left_shoulder_key_deadzone: Number = 0,
            right_shoulder_key_deadzone: Number = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            state_value_mapping: StateValueMapping = StateValueMapping.DEFAULT,
            # ##### CORE #####
            enforce_update: bool = True,
            trigger_change_after_all_values_set: bool = True,
    ):

        self._connection_state: Final[State[Connection]] = State(name=EventType.CONNECTION_CHANGE, ignore_none=False)

        self._read_states: Final[ReadStates] = ReadStates(
            left_joystick_deadzone=left_joystick_deadzone,
            right_joystick_deadzone=right_joystick_deadzone,
            left_shoulder_key_deadzone=left_shoulder_key_deadzone,
            right_shoulder_key_deadzone=right_shoulder_key_deadzone,
            gyroscope_threshold=gyroscope_threshold,
            accelerometer_threshold=accelerometer_threshold,
            orientation_threshold=orientation_threshold,
            state_value_mapping=state_value_mapping,
            enforce_update=enforce_update,
            trigger_change_after_all_values_set=trigger_change_after_all_values_set,
        )
        self._write_states: Final[WriteStates] = WriteStates(
            state_value_mapping=state_value_mapping,
        )

        # Hardware
        self._hid_controller_device: HidControllerDevice = HidControllerDevice(device_index_or_device_info)
        self._hid_controller_device.on_exception(self._on_thread_exception)
        self._hid_controller_device.on_in_report(self._on_in_report)

    @property
    def states(self) -> ReadStates:
        return self._read_states

    def on_battery_low(self, level_percentage: float, callback: BatteryLowCallback):
        battery_low_level_percentage: float = level_percentage

        def check(_: float | None, batt_level_percentage: float) -> None:
            if batt_level_percentage <= battery_low_level_percentage:
                callback(batt_level_percentage)

        self.states.battery_level_percent.on_change(check)

    def on_connection_change(self, callback: StateChangeCb):
        self._connection_state.on_change(callback)

    def on_exception(self, callback: ExceptionCallback):
        self._hid_controller_device.on_exception(callback)

    def on_state_change(self, state_name: ReadStateName | StateChangeCb, callback: StateChangeCb = None):
        self._read_states.on_change(state_name, callback)

    def on_any_state_change(self, callback: StateChangeCb):
        self._read_states.on_any_change(callback)

    def set_state(self, state_name: WriteStateName, value: Number):
        self._write_states.set_value_mapped(state_name, value)

    def set_motor_left(self, value: Number):
        self.set_state(WriteStateName.MOTOR_LEFT, value)

    def init(self) -> None:
        assert not self._hid_controller_device.opened, 'already opened'
        self._hid_controller_device.open()
        self._connection_state.set_value(Connection(True, self._hid_controller_device.connection_type))

    def deinit(self) -> None:
        assert self._hid_controller_device.opened, 'not opened yet'
        self._hid_controller_device.close()
        self._connection_state.set_value(Connection(False, self._hid_controller_device.connection_type))

    def _on_in_report(self, in_report: InReport) -> None:
        self._read_states.update(in_report, self._hid_controller_device.connection_type)
        if self._write_states.changed:
            # print(f'Sending report.')
            self._write_states.update_out_report(self._hid_controller_device.out_report)
            self._write_states.set_unchanged()
            self._hid_controller_device.write()

    def _on_thread_exception(self, exception: Exception) -> None:
        print('An Exception in the loop thread occured:', format_exception(exception))
