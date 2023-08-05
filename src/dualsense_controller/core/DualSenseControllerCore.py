from functools import partial
from typing import Final

from dualsense_controller.core.HidControllerDevice import HidControllerDevice
from dualsense_controller.core.enum import ConnectionType, EventType
from dualsense_controller.core.hidapi.hidapi import DeviceInfo
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.mapping.enum import StateValueMapping
from dualsense_controller.core.state.read_state.ReadStates import ReadStates
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.read_state.value_type import Battery, Connection
from dualsense_controller.core.state.typedef import Number, StateChangeCallback
from dualsense_controller.core.state.write_state.WriteStates import WriteStates
from dualsense_controller.core.state.write_state.enum import WriteStateName
from dualsense_controller.core.typedef import BatteryLowCallback, ExceptionCallback, SimpleCallback
from dualsense_controller.core.util import format_exception


class DualSenseControllerCore:

    @staticmethod
    def enumerate_devices() -> list[DeviceInfo]:
        return HidControllerDevice.enumerate_devices()

    @property
    def is_initialized(self) -> bool:
        return self._hid_controller_device.is_opened

    @property
    def read_states(self) -> ReadStates:
        return self._read_states

    @property
    def write_states(self) -> WriteStates:
        return self._write_states

    @property
    def connection_type(self) -> ConnectionType:
        return self._hid_controller_device.connection_type

    def __init__(
            self,
            # ##### BASE  #####
            device_index_or_device_info: int | DeviceInfo = 0,
            # ##### FEELING  #####
            left_joystick_deadzone: Number = 0,
            right_joystick_deadzone: Number = 0,
            l2_deadzone: Number = 0,
            r2_deadzone: Number = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            state_value_mapping: StateValueMapping = StateValueMapping.DEFAULT,
            # ##### CORE #####
            enforce_update: bool = False,
            can_update_itself: bool = True,
    ):

        self._connection_state: Final[State[Connection]] = State(name=EventType.CONNECTION_CHANGE, ignore_none=False)

        state_value_mapper: StateValueMapper = StateValueMapper(
            mapping=state_value_mapping,
            left_joystick_deadzone=left_joystick_deadzone,
            right_joystick_deadzone=right_joystick_deadzone,
            l2_deadzone=l2_deadzone,
            r2_deadzone=r2_deadzone,
            gyroscope_threshold=gyroscope_threshold,
            accelerometer_threshold=accelerometer_threshold,
            orientation_threshold=orientation_threshold,
        )

        self._read_states: Final[ReadStates] = ReadStates(
            state_value_mapper=state_value_mapper,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

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
        self.read_states.battery.on_change(partial(self._check_battery, callback, level_percentage))

    def on_connection_change(self, callback: StateChangeCallback):
        self._connection_state.on_change(callback)

    def on_exception(self, callback: ExceptionCallback):
        self._hid_controller_device.on_exception(callback)

    def on_state_change(self, state_name: ReadStateName | StateChangeCallback, callback: StateChangeCallback = None):
        self._read_states.on_change(state_name, callback)

    def on_any_state_change(self, callback: StateChangeCallback):
        self._read_states.on_any_change(callback)

    def set_state(self, state_name: WriteStateName, value: Number):
        self._write_states.set_value(state_name, value)

    def init(self) -> None:
        assert not self._hid_controller_device.is_opened, 'already opened'
        self._hid_controller_device.open()
        self._connection_state.value = Connection(True, self._hid_controller_device.connection_type)

    def deinit(self) -> None:
        assert self._hid_controller_device.is_opened, 'not opened yet'
        self._hid_controller_device.close()
        self._connection_state.value = Connection(False, self._hid_controller_device.connection_type)

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
