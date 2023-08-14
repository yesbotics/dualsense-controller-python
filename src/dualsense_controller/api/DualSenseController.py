from __future__ import annotations

import warnings
from typing import Final

from dualsense_controller.api.Properties import Properties
from dualsense_controller.api.enum import UpdateLevel
from dualsense_controller.api.property import AccelerometerProperty, BatteryProperty, BenchmarkProperty, ButtonProperty, \
    ConnectionProperty, \
    ExceptionProperty, \
    GyroscopeProperty, JoyStickProperty, \
    LightbarProperty, MicrophoneProperty, OrientationProperty, PlayerLedsProperty, RumbleProperty, \
    TouchFingerProperty, TriggerProperty
from dualsense_controller.core.DualSenseControllerCore import DualSenseControllerCore
from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.hidapi import DeviceInfo
from dualsense_controller.core.state.mapping.enum import StateValueMapping as Mapping
from dualsense_controller.core.state.typedef import Number


class DualSenseController:

    # ################################################# STATIC STUFF ##################################################

    @staticmethod
    def enumerate_devices() -> list[DeviceInfo]:
        return DualSenseControllerCore.enumerate_devices()

    # ################################################# GETTERS  MISC ##################################################

    @property
    def connection_type(self) -> ConnectionType:
        return self._core.connection_type

    @property
    def is_active(self) -> bool:
        return self._core.is_initialized

    # ############################################# GETTERS READ PROPS ##############################################

    # ############ MAIN
    @property
    def connection(self) -> ConnectionProperty:
        return self._properties.connection

    @property
    def benchmark(self) -> BenchmarkProperty:
        return self._properties.benchmark

    @property
    def exceptions(self) -> ExceptionProperty:
        return self._properties.exceptions

    @property
    def battery(self) -> BatteryProperty:
        return self._properties.battery

    # ############ BTN MISC
    @property
    def btn_ps(self) -> ButtonProperty:
        return self._properties.btn_ps

    @property
    def btn_options(self) -> ButtonProperty:
        return self._properties.btn_options

    @property
    def btn_create(self) -> ButtonProperty:
        return self._properties.btn_create

    @property
    def btn_mute(self) -> ButtonProperty:
        return self._properties.btn_mute

    @property
    def btn_touchpad(self) -> ButtonProperty:
        return self._properties.btn_touchpad

    # ############ BTN SYMBOL
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

    # ############ BTN DPAD
    @property
    def btn_left(self) -> ButtonProperty:
        return self._properties.btn_left

    @property
    def btn_up(self) -> ButtonProperty:
        return self._properties.btn_up

    @property
    def btn_right(self) -> ButtonProperty:
        return self._properties.btn_right

    @property
    def btn_down(self) -> ButtonProperty:
        return self._properties.btn_down

    # # ############ BTN L AND R
    @property
    def btn_l1(self) -> ButtonProperty:
        return self._properties.btn_l1

    @property
    def btn_r1(self) -> ButtonProperty:
        return self._properties.btn_r1

    @property
    def btn_l2(self) -> ButtonProperty:
        return self._properties.btn_l2

    @property
    def btn_r2(self) -> ButtonProperty:
        return self._properties.btn_r2

    @property
    def btn_l3(self) -> ButtonProperty:
        return self._properties.btn_l3

    @property
    def btn_r3(self) -> ButtonProperty:
        return self._properties.btn_r3

    # ############ TRIGGERS
    @property
    def left_trigger(self) -> TriggerProperty:
        return self._properties.left_trigger

    @property
    def right_trigger(self) -> TriggerProperty:
        return self._properties.right_trigger

    # ############ STICKS
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

    # ############ TOUCH
    @property
    def touch_finger_1(self) -> TouchFingerProperty:
        return self._properties.touch_finger_1

    @property
    def touch_finger_2(self) -> TouchFingerProperty:
        return self._properties.touch_finger_2

    # ############ IMU
    @property
    def gyroscope(self) -> GyroscopeProperty:
        return self._properties.gyroscope

    @property
    def accelerometer(self) -> AccelerometerProperty:
        return self._properties.accelerometer

    @property
    def orientation(self) -> OrientationProperty:
        return self._properties.orientation

    # ############################################## GETTERS WRITE PROPS ##############################################

    @property
    def left_rumble(self) -> RumbleProperty:
        return self._properties.left_rumble

    @property
    def right_rumble(self) -> RumbleProperty:
        return self._properties.right_rumble

    @property
    def player_leds(self) -> PlayerLedsProperty:
        return self._properties.player_leds

    @property
    def microphone(self) -> MicrophoneProperty:
        return self._properties.microphone

    @property
    def lightbar(self) -> LightbarProperty:
        return self._properties.lightbar

    # ################################################# MAIN #################################################

    def __init__(
            self,
            # CORE
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
            # OPTS
            microphone_initially_muted: bool = True,
            microphone_invert_led: bool = False,
    ):

        warnings.filterwarnings("always", category=UserWarning)

        self._core: DualSenseControllerCore = DualSenseControllerCore(
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
            # STATES
            self._core.connection_state,
            self._core.update_benchmark_state,
            self._core.exception_state,
            self._core.read_states,
            self._core.write_states,
            # OPTS
            microphone_invert_led=microphone_invert_led,
        )

        self._microphone_initially_muted: Final[bool] = microphone_initially_muted

    def wait_until_updated(self) -> None:
        return self._core.wait_until_updated()

    def activate(self) -> None:
        self._core.init()
        if self._microphone_initially_muted:
            self._properties.microphone.set_muted()
        else:
            self._properties.microphone.set_unmuted()
        self._properties.microphone.refresh_workaround()

    def deactivate(self) -> None:
        self._core.deinit()
