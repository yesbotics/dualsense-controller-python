from functools import partial
from typing import Final

from dualsense_controller.core.HidControllerDevice import HidControllerDevice
from dualsense_controller.core.hidapi.hidapi import DeviceInfo
from dualsense_controller.enum import EventType
from dualsense_controller.report.in_report.InReport import InReport
from dualsense_controller.state.State import State
from dualsense_controller.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.state.mapping.enum import StateValueMapping
from dualsense_controller.state.read_state.ReadStates import ReadStates
from dualsense_controller.state.read_state.RestictedStatesAccess import RestrictedStatesAccess
from dualsense_controller.state.read_state.enum import ReadStateName
from dualsense_controller.state.read_state.value_type import Battery, Connection
from dualsense_controller.state.typedef import Number, StateChangeCallback
from dualsense_controller.state.write_state.WriteStates import WriteStates
from dualsense_controller.state.write_state.enum import WriteStateName
from dualsense_controller.typedef import BatteryLowCallback, ExceptionCallback, SimpleCallback
from dualsense_controller.util import format_exception


class DualSenseController:

    @staticmethod
    def enumerate_devices() -> list[DeviceInfo]:
        return HidControllerDevice.enumerate_devices()

    @property
    def states(self) -> RestrictedStatesAccess:
        return self._restrictes_states_access

    def __init__(
            self,
            # ##### BASE  #####
            device_index_or_device_info: int | DeviceInfo = 0,
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

        state_value_mapper: StateValueMapper = StateValueMapper(
            mapping=state_value_mapping,
            left_joystick_deadzone=left_joystick_deadzone,
            right_joystick_deadzone=right_joystick_deadzone,
            left_shoulder_key_deadzone=left_shoulder_key_deadzone,
            right_shoulder_key_deadzone=right_shoulder_key_deadzone,
            gyroscope_threshold=gyroscope_threshold,
            accelerometer_threshold=accelerometer_threshold,
            orientation_threshold=orientation_threshold,
        )

        self._read_states: Final[ReadStates] = ReadStates(
            state_value_mapper=state_value_mapper,
            enforce_update=enforce_update,
            trigger_change_after_all_values_set=trigger_change_after_all_values_set,
        )
        self._restrictes_states_access: RestrictedStatesAccess = RestrictedStatesAccess(self._read_states)

        self._write_states: Final[WriteStates] = WriteStates(
            state_value_mapper=state_value_mapper,
        )

        # Hardware
        self._hid_controller_device: HidControllerDevice = HidControllerDevice(device_index_or_device_info)
        self._hid_controller_device.on_exception(self._on_thread_exception)
        self._hid_controller_device.on_in_report(self._on_in_report)

    def on_updated(self, callback: SimpleCallback) -> None:
        self._read_states.on_updated(callback)

    def on_battery_low(self, level_percentage: float, callback: BatteryLowCallback):
        self.states.battery.on_change(partial(self._check_battery, callback, level_percentage))

    def on_connection_change(self, callback: StateChangeCallback):
        self._connection_state.on_change(callback)

    def on_exception(self, callback: ExceptionCallback):
        self._hid_controller_device.on_exception(callback)

    def on_state_change(self, state_name: ReadStateName | StateChangeCallback, callback: StateChangeCallback = None):
        self._read_states.on_change(state_name, callback)

    def on_any_state_change(self, callback: StateChangeCallback):
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

    def _check_battery(self, callback: BatteryLowCallback, level_percentage: float, battery: Battery) -> None:
        if battery.level_percentage <= level_percentage:
            callback(battery.level_percentage)

    def _on_in_report(self, in_report: InReport) -> None:
        self._read_states.update(in_report, self._hid_controller_device.connection_type)
        if self._write_states.changed:
            # print(f'Sending report.')
            self._write_states.update_out_report(self._hid_controller_device.out_report)
            self._write_states.set_unchanged()
            self._hid_controller_device.write()

    def _on_thread_exception(self, exception: Exception) -> None:
        print('An Exception in the loop thread occured:', format_exception(exception))
