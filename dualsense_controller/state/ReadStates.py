from typing import Final

from dualsense_controller import ConnectionType
from dualsense_controller.report import InReport
from dualsense_controller.state import (
    Accelerometer, AnyStateChangeCallback, BaseStates, Gyroscope, JoyStick,
    Orientation, ReadStateName, RestrictedStateAccess, State, StateChangeCallback
)


def _compare_joystick(before: JoyStick, after: JoyStick, deadzone: int = 0, threshold: int = 0) -> bool:
    # if before is None or abs(value - old_value) >= self._threshold:
    #     self._change_value(old_value=old_value, new_value=value)
    return before != after


def _compare_shoulder_key(before: int, after: int, deadzone: int = 0, threshold: int = 0) -> bool:
    return before != after


def _compare_gyroscope(before: Gyroscope, after: Gyroscope, threshold: int = 0) -> bool:
    return before != after


def _compare_accelerometer(before: Accelerometer, after: Accelerometer, threshold: int = 0) -> bool:
    return before != after


def _compare_orientation(before: Orientation, after: Orientation, threshold: int = 0) -> bool:
    return before != after


class ReadStates(BaseStates[ReadStateName]):

    def __init__(
            self,
            joystick_threshold: int = 0,
            joystick_deadzone: int = 0,
            shoulder_key_threshold: int = 0,
            shoulder_key_deadzone: int = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
    ):
        super().__init__()

        # STICKS
        self._left_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X
        )
        self._left_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y,
        )
        self._left_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK,
            compare_fn=_compare_joystick,
            threshold=joystick_threshold,
            deadzone=joystick_deadzone,
        )
        self._right_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X,
        )
        self._right_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y,
        )
        self._right_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK,
            compare_fn=_compare_joystick,
            threshold=joystick_threshold,
            deadzone=joystick_deadzone,
        )

        # GYRO, ACCEL, ORIENT
        self._gyroscope_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_X
        )
        self._gyroscope_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Y
        )
        self._gyroscope_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Z
        )
        self._gyroscope: Final[State[Gyroscope]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE,
            compare_fn=_compare_gyroscope,
            threshold=gyroscope_threshold,
        )
        self._accelerometer_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_X
        )
        self._accelerometer_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Y
        )
        self._accelerometer_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Z
        )
        self._accelerometer: Final[State[Accelerometer]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER,
            compare_fn=_compare_accelerometer,
            threshold=accelerometer_threshold,
        )
        self._orientation: Final[State[Orientation]] = self._create_and_register_state(
            ReadStateName.ORIENTATION, compare_fn=_compare_orientation
        )

        # SHOULDER KEYS
        self._l2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2,
            compare_fn=_compare_shoulder_key,
            threshold=shoulder_key_threshold,
            deadzone=shoulder_key_deadzone,
        )
        self._r2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2,
            compare_fn=_compare_shoulder_key,
            threshold=shoulder_key_threshold,
            deadzone=shoulder_key_deadzone,
        )

        # DIG BTN
        self._btn_up: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_UP)
        self._btn_left: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_LEFT
        )
        self._btn_down: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_DOWN
        )
        self._btn_right: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_RIGHT
        )
        self._btn_square: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_SQUARE
        )
        self._btn_cross: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CROSS
        )
        self._btn_circle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CIRCLE
        )
        self._btn_triangle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TRIANGLE
        )
        self._btn_l1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L1
        )
        self._btn_r1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R1
        )
        self._btn_l2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L2
        )
        self._btn_r2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R2
        )
        self._btn_create: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CREATE
        )
        self._btn_options: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_OPTIONS
        )
        self._btn_l3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L3
        )
        self._btn_r3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R3
        )
        self._btn_ps: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_PS
        )
        self._btn_touchpad: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TOUCHPAD
        )
        self._btn_mute: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_MUTE
        )

        # TOUCH
        self._touch_0_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ACTIVE
        )
        self._touch_0_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ID
        )
        self._touch_0_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_X
        )
        self._touch_0_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_Y
        )
        self._touch_1_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ACTIVE
        )
        self._touch_1_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ID
        )
        self._touch_1_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_X
        )
        self._touch_1_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_Y
        )

        # FEEDBACK
        self._l2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_ACTIVE
        )
        self._l2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_VALUE
        )
        self._r2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_ACTIVE
        )
        self._r2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_VALUE
        )

        # BATT
        self._battery_level_percent: Final[State[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT, ignore_initial_none=False
        )
        self._battery_full: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL, ignore_initial_none=False
        )
        self._battery_charging: Final[State[int]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING, ignore_initial_none=False
        )

    def on_change(self, name_or_callback: ReadStateName | AnyStateChangeCallback, callback: StateChangeCallback = None):
        if callback is None:
            self.on_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).on_change(callback)

    def on_any_change(self, callback: AnyStateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.on_change(callback)

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        # ##### ANALOG STICKS #####

        if self._left_stick.has_listeners or self._left_stick_x.has_listeners:
            self._left_stick_x.value = in_report.axes_0
        if self._left_stick.has_listeners or self._left_stick_y.has_listeners:
            self._left_stick_y.value = in_report.axes_1
        if self._left_stick.has_listeners and (self._left_stick_x.changed or self._left_stick_y.changed):
            self._left_stick.value = JoyStick(x=self._left_stick_x.value, y=self._left_stick_y.value)

        if self._right_stick.has_listeners or self._right_stick_x.has_listeners:
            self._right_stick_x.value = in_report.axes_2
        if self._right_stick.has_listeners or self._right_stick_y.has_listeners:
            self._right_stick_y.value = in_report.axes_3
        if self._right_stick.has_listeners and (self._right_stick_x.changed or self._right_stick_y.changed):
            self._right_stick.value = JoyStick(x=self._right_stick_x.value, y=self._right_stick_y.value)

        if self._l2.has_listeners:
            self._l2.value = in_report.axes_4

        if self._r2.has_listeners:
            self._r2.value = in_report.axes_5

        # ##### BUTTONS #####
        dpad: int = in_report.buttons_0 & 0x0f
        if self._btn_up.has_listeners:
            self._btn_up.value = dpad == 0 or dpad == 1 or dpad == 7
        if self._btn_down.has_listeners:
            self._btn_down.value = dpad == 3 or dpad == 4 or dpad == 5
        if self._btn_left.has_listeners:
            self._btn_left.value = dpad == 5 or dpad == 6 or dpad == 7
        if self._btn_right.has_listeners:
            self._btn_right.value = dpad == 1 or dpad == 2 or dpad == 3
        if self._btn_square.has_listeners:
            self._btn_square.value = bool(in_report.buttons_0 & 0x10)
        if self._btn_cross.has_listeners:
            self._btn_cross.value = bool(in_report.buttons_0 & 0x20)
        if self._btn_circle.has_listeners:
            self._btn_circle.value = bool(in_report.buttons_0 & 0x40)
        if self._btn_triangle.has_listeners:
            self._btn_triangle.value = bool(in_report.buttons_0 & 0x80)
        if self._btn_l1.has_listeners:
            self._btn_l1.value = bool(in_report.buttons_1 & 0x01)
        if self._btn_r1.has_listeners:
            self._btn_r1.value = bool(in_report.buttons_1 & 0x02)
        if self._btn_l2.has_listeners:
            self._btn_l2.value = bool(in_report.buttons_1 & 0x04)
        if self._btn_r2.has_listeners:
            self._btn_r2.value = bool(in_report.buttons_1 & 0x08)
        if self._btn_create.has_listeners:
            self._btn_create.value = bool(in_report.buttons_1 & 0x10)
        if self._btn_options.has_listeners:
            self._btn_options.value = bool(in_report.buttons_1 & 0x20)
        if self._btn_l3.has_listeners:
            self._btn_l3.value = bool(in_report.buttons_1 & 0x40)
        if self._btn_r3.has_listeners:
            self._btn_r3.value = bool(in_report.buttons_1 & 0x80)
        if self._btn_ps.has_listeners:
            self._btn_ps.value = bool(in_report.buttons_2 & 0x01)
        if self._btn_mute.has_listeners:
            self._btn_mute.value = bool(in_report.buttons_2 & 0x04)
        if self._btn_touchpad.has_listeners:
            self._btn_touchpad.value = bool(in_report.buttons_2 & 0x02)

        # following not supported for BT01
        if connection_type == ConnectionType.BT_01:
            return

        # ##### GYRO #####
        if self._gyroscope.has_listeners or self._gyroscope_x.has_listeners:
            gyro_x: int = (in_report.gyro_x_1 << 8) | in_report.gyro_x_0
            if gyro_x > 0x7FFF:
                gyro_x -= 0x10000
            self._gyroscope_x.value = gyro_x
        if self._gyroscope.has_listeners or self._gyroscope_y.has_listeners:
            gyro_y: int = (in_report.gyro_y_1 << 8) | in_report.gyro_y_0
            if gyro_y > 0x7FFF:
                gyro_y -= 0x10000
            self._gyroscope_y.value = gyro_y
        if self._gyroscope.has_listeners or self._gyroscope_z.has_listeners:
            gyro_z: int = (in_report.gyro_z_1 << 8) | in_report.gyro_z_0
            if gyro_z > 0x7FFF:
                gyro_z -= 0x10000
            self._gyroscope_z.value = gyro_z

        if self._gyroscope.has_listeners \
                and (self._gyroscope_x.changed or self._gyroscope_y.changed or self._gyroscope_z.changed):
            self._gyroscope.value = Gyroscope(
                x=self._gyroscope_x.value,
                y=self._gyroscope_y.value,
                z=self._gyroscope_z.value,
            )

        # ##### ACCEL #####
        if self._accelerometer.has_listeners or self._accelerometer_x.has_listeners:
            accel_x: int = (in_report.accel_x_1 << 8) | in_report.accel_x_0
            if accel_x > 0x7FFF:
                accel_x -= 0x10000
            self._accelerometer_x.value = accel_x
        if self._accelerometer.has_listeners or self._accelerometer_y.has_listeners:
            accel_y: int = (in_report.accel_y_1 << 8) | in_report.accel_y_0
            if accel_y > 0x7FFF:
                accel_y -= 0x10000
            self._accelerometer_y.value = accel_y
        if self._accelerometer.has_listeners or self._accelerometer_z.has_listeners:
            accel_z: int = (in_report.accel_z_1 << 8) | in_report.accel_z_0
            if accel_z > 0x7FFF:
                accel_z -= 0x10000
            self._accelerometer_z.value = accel_z

        if self._accelerometer.has_listeners \
                and (self._accelerometer_x.changed or self._accelerometer_y.changed or self._accelerometer_z.changed):
            self._accelerometer.value = Accelerometer(
                x=self._accelerometer_x.value,
                y=self._accelerometer_y.value,
                z=self._accelerometer_z.value,
            )

        # ##### ORIENTATION #####
        if self._orientation.has_listeners and (self._accelerometer.changed or self._gyroscope.changed):
            # o = calculate_orientation(
            #     [self._gyroscope_x.value],
            #     [self._gyroscope_y.value],
            #     [self._gyroscope_z.value],
            #     self._accelerometer_x.value,
            #     self._accelerometer_y.value,
            #     self._accelerometer_z.value,
            # )
            # orientation: Orientation = Orientation(
            #     yaw=0,
            #     pitch=0,
            #     roll=0,
            # )
            # self._orientation.value = orientation
            pass

        # ##### TOUCH #####
        touch_0_active: bool = False
        if self._touch_0_active.has_listeners:
            touch_0_active = not (in_report.touch_0_0 & 0x80)
            self._touch_0_active.value = touch_0_active
        if touch_0_active and self._touch_0_id.has_listeners:
            self._touch_0_id.value = (in_report.touch_0_0 & 0x7F)
        if touch_0_active and self._touch_0_x.has_listeners:
            self._touch_0_x.value = ((in_report.touch_0_2 & 0x0F) << 8) | in_report.touch_0_1
        if touch_0_active and self._touch_0_y.has_listeners:
            self._touch_0_y.value = (in_report.touch_0_3 << 4) | ((in_report.touch_0_2 & 0xF0) >> 4)

        touch_1_active: bool = False
        if self._touch_1_active.has_listeners:
            touch_1_active = not (in_report.touch_1_0 & 0x80)
            self._touch_1_active.value = touch_1_active
        if touch_1_active and self._touch_1_id.has_listeners:
            self._touch_1_id.value = (in_report.touch_1_0 & 0x7F)
        if touch_1_active and self._touch_1_x.has_listeners:
            self._touch_1_x.value = ((in_report.touch_1_2 & 0x0F) << 8) | in_report.touch_1_1
        if touch_1_active and self._touch_1_y.has_listeners:
            self._touch_1_y.value = (in_report.touch_1_3 << 4) | ((in_report.touch_1_2 & 0xF0) >> 4)

        # ##### TRIGGER FEEDBACK #####
        if self._l2_feedback_active.has_listeners:
            self._l2_feedback_active.value = bool(in_report.l2_feedback & 0x10)
        if self._l2_feedback_value.has_listeners:
            self._l2_feedback_value.value = in_report.l2_feedback & 0xff
        if self._r2_feedback_active.has_listeners:
            self._r2_feedback_active.value = bool(in_report.r2_feedback & 0x10)
        if self._r2_feedback_value.has_listeners:
            self._r2_feedback_value.value = in_report.r2_feedback & 0xff

        # ##### BATTERY #####
        if self._battery_level_percent.has_listeners:
            batt_level_raw: int = in_report.battery_0 & 0x0f
            if batt_level_raw > 8:
                batt_level_raw = 8
            batt_level: float = batt_level_raw / 8
            self._battery_level_percent.value = batt_level * 100
        if self._battery_full.has_listeners:
            self._battery_full.value = not not (in_report.battery_0 & 0x20)
        if self._battery_charging.has_listeners:
            self._battery_charging.value = not not (in_report.battery_1 & 0x08)

    def remove_change_listener(
            self, name_or_callback: ReadStateName | AnyStateChangeCallback, callback: StateChangeCallback = None
    ) -> None:
        if isinstance(name_or_callback, ReadStateName):
            self._get_state_by_name(name_or_callback).remove_change_listener(callback)
        elif callable(name_or_callback):
            self.remove_any_change_listener(name_or_callback)
        else:
            self.remove_all_change_listeners()

    def remove_all_change_listeners(self) -> None:
        for state_name, state in self._states_dict.items():
            state.remove_all_change_listeners()

    def remove_any_change_listener(self, callback: AnyStateChangeCallback) -> None:
        for state_name, state in self._states_dict.items():
            state.remove_change_listener(callback)

    @property
    def left_stick_x(self) -> RestrictedStateAccess[int]:
        return self._left_stick_x.restricted_access

    @property
    def left_stick_y(self) -> RestrictedStateAccess[int]:
        return self._left_stick_y.restricted_access

    @property
    def right_stick_x(self) -> RestrictedStateAccess[int]:
        return self._right_stick_x.restricted_access

    @property
    def right_stick_y(self) -> RestrictedStateAccess[int]:
        return self._right_stick_y.restricted_access

    @property
    def l2(self) -> RestrictedStateAccess[int]:
        return self._l2.restricted_access

    @property
    def r2(self) -> RestrictedStateAccess[int]:
        return self._r2.restricted_access

    @property
    def btn_up(self) -> RestrictedStateAccess[bool]:
        return self._btn_up.restricted_access

    @property
    def btn_left(self) -> RestrictedStateAccess[bool]:
        return self._btn_left.restricted_access

    @property
    def btn_down(self) -> RestrictedStateAccess[bool]:
        return self._btn_down.restricted_access

    @property
    def btn_right(self) -> RestrictedStateAccess[bool]:
        return self._btn_right.restricted_access

    @property
    def btn_square(self) -> RestrictedStateAccess[bool]:
        return self._btn_square.restricted_access

    @property
    def btn_cross(self) -> RestrictedStateAccess[bool]:
        return self._btn_cross.restricted_access

    @property
    def btn_circle(self) -> RestrictedStateAccess[bool]:
        return self._btn_circle.restricted_access

    @property
    def btn_triangle(self) -> RestrictedStateAccess[bool]:
        return self._btn_triangle.restricted_access

    @property
    def btn_l1(self) -> RestrictedStateAccess[bool]:
        return self._btn_l1.restricted_access

    @property
    def btn_r1(self) -> RestrictedStateAccess[bool]:
        return RestrictedStateAccess(self._btn_r1)

    @property
    def btn_l2(self) -> RestrictedStateAccess[bool]:
        return self._btn_l2.restricted_access

    @property
    def btn_r2(self) -> RestrictedStateAccess[bool]:
        return self._btn_r2.restricted_access

    @property
    def btn_create(self) -> RestrictedStateAccess[bool]:
        return self._btn_create.restricted_access

    @property
    def btn_options(self) -> RestrictedStateAccess[bool]:
        return self._btn_options.restricted_access

    @property
    def btn_l3(self) -> RestrictedStateAccess[bool]:
        return self._btn_l3.restricted_access

    @property
    def btn_r3(self) -> RestrictedStateAccess[bool]:
        return self._btn_r3.restricted_access

    @property
    def btn_ps(self) -> RestrictedStateAccess[bool]:
        return self._btn_ps.restricted_access

    @property
    def btn_touchpad(self) -> RestrictedStateAccess[bool]:
        return self._btn_touchpad.restricted_access

    @property
    def btn_mute(self) -> RestrictedStateAccess[bool]:
        return self._btn_mute.restricted_access

    @property
    def gyroscope_x(self) -> RestrictedStateAccess[int]:
        return self._gyroscope_x.restricted_access

    @property
    def gyroscope_y(self) -> RestrictedStateAccess[int]:
        return self._gyroscope_y.restricted_access

    @property
    def gyroscope_z(self) -> RestrictedStateAccess[int]:
        return self._gyroscope_z.restricted_access

    @property
    def accelerometer_x(self) -> RestrictedStateAccess[int]:
        return self._accelerometer_x.restricted_access

    @property
    def accelerometer_y(self) -> RestrictedStateAccess[int]:
        return self._accelerometer_y.restricted_access

    @property
    def accelerometer_z(self) -> RestrictedStateAccess[int]:
        return self._accelerometer_z.restricted_access

    @property
    def touch_0_active(self) -> RestrictedStateAccess[bool]:
        return self._touch_0_active.restricted_access

    @property
    def touch_0_id(self) -> RestrictedStateAccess[int]:
        return self._touch_0_id.restricted_access

    @property
    def touch_0_x(self) -> RestrictedStateAccess[int]:
        return self._touch_0_x.restricted_access

    @property
    def touch_0_y(self) -> RestrictedStateAccess[int]:
        return self._touch_0_y.restricted_access

    @property
    def touch_1_active(self) -> RestrictedStateAccess[bool]:
        return self._touch_1_active.restricted_access

    @property
    def touch_1_id(self) -> RestrictedStateAccess[int]:
        return self._touch_1_id.restricted_access

    @property
    def touch_1_x(self) -> RestrictedStateAccess[int]:
        return self._touch_1_x.restricted_access

    @property
    def touch_1_y(self) -> RestrictedStateAccess[int]:
        return self._touch_1_y.restricted_access

    @property
    def l2_feedback_active(self) -> RestrictedStateAccess[bool]:
        return self._l2_feedback_active.restricted_access

    @property
    def l2_feedback_value(self) -> RestrictedStateAccess[int]:
        return self._l2_feedback_value.restricted_access

    @property
    def r2_feedback_active(self) -> RestrictedStateAccess[bool]:
        return self._r2_feedback_active.restricted_access

    @property
    def r2_feedback_value(self) -> RestrictedStateAccess[int]:
        return self._r2_feedback_value.restricted_access

    @property
    def battery_level_percent(self) -> RestrictedStateAccess[float]:
        return self._battery_level_percent.restricted_access

    @property
    def battery_full(self) -> RestrictedStateAccess[bool]:
        return self._battery_full.restricted_access

    @property
    def battery_charging(self) -> RestrictedStateAccess[int]:
        return self._battery_charging.restricted_access

    # ####### COMPLEX ########
    @property
    def left_stick(self) -> RestrictedStateAccess[JoyStick]:
        return self._left_stick.restricted_access

    @property
    def right_stick(self) -> RestrictedStateAccess[JoyStick]:
        return self._right_stick.restricted_access

    @property
    def gyroscope(self) -> RestrictedStateAccess[Gyroscope]:
        return self._gyroscope.restricted_access

    @property
    def accelerometer(self) -> RestrictedStateAccess[Accelerometer]:
        return self._accelerometer.restricted_access

    @property
    def orientation(self) -> RestrictedStateAccess[Orientation]:
        return self._orientation.restricted_access
