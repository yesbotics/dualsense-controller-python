from __future__ import annotations

from typing import Final

from dualsense_controller.api.Properties import Properties
from dualsense_controller.api.enum import UpdateLevel
from dualsense_controller.api.property import BatteryProperty, BenchmarkProperty, ButtonProperty, ConnectionProperty, \
    ExceptionProperty, \
    JoyStickProperty, \
    RumbleProperty, \
    TriggerProperty
from dualsense_controller.core.DualSenseControllerCore import DualSenseControllerCore
from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.hidapi import DeviceInfo
from dualsense_controller.core.state.mapping.enum import StateValueMapping as Mapping
from dualsense_controller.core.state.typedef import Number
from dualsense_controller.core.typedef import EmptyCallback, ExceptionCallback, UpdateBenchmarkCallback


class DualSenseController:
    # ################################################# STATIC STUFF ##################################################

    @staticmethod
    def enumerate_devices() -> list[DeviceInfo]:
        return DualSenseControllerCore.enumerate_devices()

    # ################################################# GETTERS  MISC ##################################################

    @property
    def connection_type(self) -> ConnectionType:
        return self._dsc.connection_type

    @property
    def is_active(self) -> bool:
        return self._dsc.is_initialized

    # ############################################# GETTERS READ PROPS ##############################################

    @property
    def btn_cross(self) -> ButtonProperty:
        return self._properties.btn_cross

    @property
    def btn_square(self) -> ButtonProperty:
        return self._properties.btn_square

    @property
    def btn_triangle(self) -> ButtonProperty:
        return self._properties.btn_triangle

    @property
    def btn_circle(self) -> ButtonProperty:
        return self._properties.btn_circle

    @property
    def left_trigger(self) -> TriggerProperty:
        return self._properties.left_trigger

    @property
    def right_trigger(self) -> TriggerProperty:
        return self._properties.right_trigger

    @property
    def left_stick_x(self) -> JoyStickProperty:
        return self._properties.left_stick_x

    @property
    def left_stick_y(self) -> JoyStickProperty:
        return self._properties.left_stick_y

    @property
    def left_stick(self) -> JoyStickProperty:
        return self._properties.left_stick

    @property
    def right_stick_x(self) -> JoyStickProperty:
        return self._properties.right_stick_x

    @property
    def right_stick_y(self) -> JoyStickProperty:
        return self._properties.right_stick_y

    @property
    def right_stick(self) -> JoyStickProperty:
        return self._properties.right_stick

    @property
    def battery(self) -> BatteryProperty:
        return self._properties.battery

    # ############################################## GETTERS WRITE PROPS ##############################################
    @property
    def left_rumble(self) -> RumbleProperty:
        return self._properties.left_rumble

    @property
    def right_rumble(self) -> RumbleProperty:
        return self._properties.right_rumble

    # ############################################ GETTERS SPECIAL PROPS ############################################
    @property
    def connection(self) -> ConnectionProperty:
        return self._properties.connection

    @property
    def benchmark(self) -> BenchmarkProperty:
        return self._properties.benchmark

    @property
    def exceptions(self) -> ExceptionProperty:
        return self._properties.exceptions

    # ################################################# MAIN #################################################

    def __init__(
            self,
            device_index_or_device_info: int | DeviceInfo = 0,
            left_joystick_deadzone: Number = 0.05,
            right_joystick_deadzone: Number = 0.05,
            left_trigger_deadzone: Number = 0,
            right_trigger_deadzone: Number = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            mapping: Mapping = Mapping.NORMALIZED,
            update_level: UpdateLevel = UpdateLevel.DEFAULT,
    ):
        self._dsc: DualSenseControllerCore = DualSenseControllerCore(
            device_index_or_device_info=device_index_or_device_info,
            left_joystick_deadzone=left_joystick_deadzone,
            right_joystick_deadzone=right_joystick_deadzone,
            left_trigger_deadzone=left_trigger_deadzone,
            right_trigger_deadzone=right_trigger_deadzone,
            gyroscope_threshold=gyroscope_threshold,
            accelerometer_threshold=accelerometer_threshold,
            orientation_threshold=orientation_threshold,
            state_value_mapping=mapping,
            enforce_update=update_level.value.enforce_update,
            can_update_itself=update_level.value.can_update_itself,
        )

        self._properties: Properties = Properties(
            self._dsc.connection_state,
            self._dsc.update_benchmark_state,
            self._dsc.exception_state,
            self._dsc.read_states,
            self._dsc.write_states,
        )

    def wait_until_updated(self) -> None:
        return self._dsc.wait_until_updated()

    def activate(self) -> None:
        self._dsc.init()

    def deactivate(self) -> None:
        self._dsc.deinit()
