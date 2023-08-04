from __future__ import annotations

from dualsense_controller.api.Properties import Properties
from dualsense_controller.api.property import ButtonProperty, RumbleProperty, TriggerProperty
from dualsense_controller.core.DualSenseControllerCore import DualSenseControllerCore
from dualsense_controller.core.hidapi import DeviceInfo
from dualsense_controller.core.state.mapping.enum import StateValueMapping as Mapping
from dualsense_controller.core.state.typedef import Number
from dualsense_controller.core.typedef import ExceptionCallback


class DualSenseController:

    @staticmethod
    def enumerate_devices() -> list[DeviceInfo]:
        return DualSenseControllerCore.enumerate_devices()

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
    def left_rumble(self) -> RumbleProperty:
        return self._properties.left_rumble

    @property
    def right_rumble(self) -> RumbleProperty:
        return self._properties.right_rumble

    def __init__(
            self,
            device_index_or_device_info: int | DeviceInfo = 0,
            left_joystick_deadzone: Number = 2,
            right_joystick_deadzone: Number = 2,
            l2_deadzone: Number = 0,
            r2_deadzone: Number = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            mapping: Mapping = Mapping.NORMALIZED,
            enforce_update: bool = False,
            trigger_change_after_all_values_set: bool = True,
    ):
        self._dsc: DualSenseControllerCore = DualSenseControllerCore(
            device_index_or_device_info=device_index_or_device_info,
            left_joystick_deadzone=left_joystick_deadzone,
            right_joystick_deadzone=right_joystick_deadzone,
            l2_deadzone=l2_deadzone,
            r2_deadzone=r2_deadzone,
            gyroscope_threshold=gyroscope_threshold,
            accelerometer_threshold=accelerometer_threshold,
            orientation_threshold=orientation_threshold,
            state_value_mapping=mapping,
            enforce_update=enforce_update,
            trigger_change_after_all_values_set=trigger_change_after_all_values_set,
        )
        self._properties: Properties = Properties(
            self._dsc.read_states,
            self._dsc.write_states,
        )

    def on_exception(self, callback: ExceptionCallback) -> None:
        self._dsc.on_exception(callback)

    def start(self) -> None:
        self._dsc.init()

    def stop(self) -> None:
        self._dsc.deinit()
