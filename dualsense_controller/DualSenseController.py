from typing import Final

import pyee as pyee

from dualsense_controller import HidControllerDevice
from dualsense_controller.report import InReport
from dualsense_controller.state import (
    Number, ReadStateName, ReadStates,
    StateChangeCb, StateDeterminationLevel, StateValueMapping, WriteStateName, WriteStates
)
from dualsense_controller.util import format_exception
from .enums import EventType
from .typedef import BatteryLowCallback, ConnectionChangeCallback, ExceptionCallback


class DualSenseController:

    def __init__(
            self,
            # ##### BASE  #####
            device_index: int = 0,
            # ##### FEELING  #####
            joystick_deadzone: int = 0,
            shoulder_key_deadzone: int = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            state_value_mapping: StateValueMapping = StateValueMapping.DEFAULT,
            # ##### CORE #####
            state_determination: StateDeterminationLevel = StateDeterminationLevel.LISTENER,
            trigger_change_after_all_values_set: bool = True,
    ):
        # Emitability
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()

        # State
        self._read_states: Final[ReadStates] = ReadStates(
            joystick_deadzone=joystick_deadzone,
            shoulder_key_deadzone=shoulder_key_deadzone,
            gyroscope_threshold=gyroscope_threshold,
            accelerometer_threshold=accelerometer_threshold,
            orientation_threshold=orientation_threshold,
            state_value_mapping=state_value_mapping,
            trigger_change_after_all_values_set=trigger_change_after_all_values_set,
            state_determination=state_determination,
        )
        self._write_states: Final[WriteStates] = WriteStates(
            state_value_mapping=state_value_mapping,
        )

        # Hardware
        self._hid_controller_device: HidControllerDevice = HidControllerDevice(device_index)
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

    def on_connection_change(self, callback: ConnectionChangeCallback):
        self._event_emitter.on(EventType.CONNECTION_CHANGE, callback)

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
        self._event_emitter.emit(EventType.CONNECTION_CHANGE, True, self._hid_controller_device.connection_type)

    def deinit(self) -> None:
        assert self._hid_controller_device.opened, 'not opened yet'
        connection_type = self._hid_controller_device.connection_type
        self._hid_controller_device.close()
        self._event_emitter.emit(EventType.CONNECTION_CHANGE, False, connection_type)

    def _on_in_report(self, in_report: InReport) -> None:
        self._read_states.update(in_report, self._hid_controller_device.connection_type)
        if self._write_states.changed:
            # print(f'Sending report.')
            self._write_states.update_out_report(self._hid_controller_device.out_report)
            self._write_states.set_unchanged()
            self._hid_controller_device.write()

    def _on_thread_exception(self, exception: Exception) -> None:
        print('An Exception in the loop thread occured:', format_exception(exception))
