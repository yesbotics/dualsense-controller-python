from __future__ import annotations

from typing import Final, Generic, Callable

from dualsense_controller import State, BaseStates
from dualsense_controller.common import (
    ReadStateName,
    StateChangeCallback,
    AnyStateChangeCallback,
    ConnectionType,
    StateValueType
)
from dualsense_controller.reports import InReport


class _StatePublicAccess(Generic[StateValueType]):
    def __init__(self, state: State[StateValueType]):
        self._state = state

    @property
    def value(self) -> StateValueType:
        return self._state.value

    @property
    def on_change(self) -> Callable[[StateChangeCallback], None]:
        return self._state.on_change

    @property
    def threshold(self) -> int:
        return self._state.threshold

    @threshold.setter
    def threshold(self, threshold: int) -> None:
        self._state.threshold = threshold


class ReadStates(BaseStates[ReadStateName]):

    def __init__(
            self,
            analog_threshold: int = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
    ):
        super().__init__()
        self._analog_threshold: int = analog_threshold
        self._gyroscope_threshold: int = gyroscope_threshold
        self._accelerometer_threshold: int = accelerometer_threshold

        self._left_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X, threshold=analog_threshold
        )
        self._left_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y, threshold=analog_threshold
        )
        self._right_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X, threshold=analog_threshold
        )
        self._right_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y, threshold=analog_threshold
        )
        self._l2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2, threshold=analog_threshold
        )
        self._r2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2, threshold=analog_threshold
        )
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
        self._gyroscope_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_X, threshold=gyroscope_threshold
        )
        self._gyroscope_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Y, threshold=gyroscope_threshold
        )
        self._gyroscope_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Z, threshold=gyroscope_threshold
        )
        self._accelerometer_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_X, threshold=accelerometer_threshold
        )
        self._accelerometer_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Y, threshold=accelerometer_threshold
        )
        self._accelerometer_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Z, threshold=accelerometer_threshold
        )
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
        self._battery_level_percent: Final[State[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT, skip_none=False
        )
        self._battery_full: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL, skip_none=False
        )
        self._battery_charging: Final[State[int]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING, skip_none=False
        )

    @property
    def analog_threshold(self) -> int:
        return self._analog_threshold

    @analog_threshold.setter
    def analog_threshold(self, analog_threshold: int) -> None:
        self._analog_threshold = analog_threshold
        self._left_stick_x.threshold = analog_threshold
        self._left_stick_y.threshold = analog_threshold
        self._right_stick_x.threshold = analog_threshold
        self._right_stick_y.threshold = analog_threshold
        self._l2.threshold = analog_threshold
        self._r2.threshold = analog_threshold

    @property
    def accelerometer_threshold(self) -> int:
        return self._accelerometer_threshold

    @accelerometer_threshold.setter
    def accelerometer_threshold(self, accelerometer_threshold: int) -> None:
        self._accelerometer_threshold = accelerometer_threshold
        self._accelerometer_x.threshold = accelerometer_threshold
        self._accelerometer_y.threshold = accelerometer_threshold
        self._accelerometer_z.threshold = accelerometer_threshold

    @property
    def gyroscope_threshold(self) -> int:
        return self._gyroscope_threshold

    @gyroscope_threshold.setter
    def gyroscope_threshold(self, gyroscope_threshold: int) -> None:
        self._gyroscope_threshold = gyroscope_threshold
        self._gyroscope_x.threshold = gyroscope_threshold
        self._gyroscope_y.threshold = gyroscope_threshold
        self._gyroscope_z.threshold = gyroscope_threshold

    def on_change(self, name_or_callback: ReadStateName | AnyStateChangeCallback, callback: StateChangeCallback = None):
        if callback is None:
            self.on_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).on_change(callback)

    def on_any_change(self, callback: AnyStateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.on_change(lambda old_value, new_value: callback(state_name, old_value, new_value))

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        # ##### ANALOG STICKS #####
        self._left_stick_x.value = in_report.axes_0
        self._left_stick_y.value = in_report.axes_1
        self._right_stick_x.value = in_report.axes_2
        self._right_stick_y.value = in_report.axes_3
        self._l2.value = in_report.axes_4
        self._r2.value = in_report.axes_5

        # ##### BUTTONS #####
        dpad: int = in_report.buttons_0 & 0x0f
        self._btn_up.value = dpad == 0 or dpad == 1 or dpad == 7
        self._btn_down.value = dpad == 3 or dpad == 4 or dpad == 5
        self._btn_left.value = dpad == 5 or dpad == 6 or dpad == 7
        self._btn_right.value = dpad == 1 or dpad == 2 or dpad == 3
        self._btn_square.value = bool(in_report.buttons_0 & 0x10)
        self._btn_cross.value = bool(in_report.buttons_0 & 0x20)
        self._btn_circle.value = bool(in_report.buttons_0 & 0x40)
        self._btn_triangle.value = bool(in_report.buttons_0 & 0x80)
        self._btn_l1.value = bool(in_report.buttons_1 & 0x01)
        self._btn_r1.value = bool(in_report.buttons_1 & 0x02)
        self._btn_l2.value = bool(in_report.buttons_1 & 0x04)
        self._btn_r2.value = bool(in_report.buttons_1 & 0x08)
        self._btn_create.value = bool(in_report.buttons_1 & 0x10)
        self._btn_options.value = bool(in_report.buttons_1 & 0x20)
        self._btn_l3.value = bool(in_report.buttons_1 & 0x40)
        self._btn_r3.value = bool(in_report.buttons_1 & 0x80)
        self._btn_ps.value = bool(in_report.buttons_2 & 0x01)
        self._btn_touchpad.value = bool(in_report.buttons_2 & 0x02)
        self._btn_mute.value = bool(in_report.buttons_2 & 0x04)

        # following not supported for BT01
        if connection_type == ConnectionType.BT_01:
            return

        # ##### GYRO #####
        gyro_x: int = (in_report.gyro_x_1 << 8) | in_report.gyro_x_0
        if gyro_x > 0x7FFF:
            gyro_x -= 0x10000
        gyro_y: int = (in_report.gyro_y_1 << 8) | in_report.gyro_y_0
        if gyro_y > 0x7FFF:
            gyro_y -= 0x10000
        gyro_z: int = (in_report.gyro_z_1 << 8) | in_report.gyro_z_0
        if gyro_z > 0x7FFF:
            gyro_z -= 0x10000
        self._gyroscope_x.value = gyro_x
        self._gyroscope_y.value = gyro_y
        self._gyroscope_z.value = gyro_z

        # ##### ACCEL #####
        accel_x: int = (in_report.accel_x_1 << 8) | in_report.accel_x_0
        if accel_x > 0x7FFF:
            accel_x -= 0x10000
        accel_y: int = (in_report.accel_y_1 << 8) | in_report.accel_y_0
        if accel_y > 0x7FFF:
            accel_y -= 0x10000
        accel_z: int = (in_report.accel_z_1 << 8) | in_report.accel_z_0
        if accel_z > 0x7FFF:
            accel_z -= 0x10000
        self._accelerometer_x.value = accel_x
        self._accelerometer_y.value = accel_y
        self._accelerometer_z.value = accel_z

        # ##### TOUCH #####
        self._touch_0_active.value = not (in_report.touch_0_0 & 0x80)
        self._touch_0_id.value = (in_report.touch_0_0 & 0x7F)
        self._touch_0_x.value = ((in_report.touch_0_2 & 0x0F) << 8) | in_report.touch_0_1
        self._touch_0_y.value = (in_report.touch_0_3 << 4) | ((in_report.touch_0_2 & 0xF0) >> 4)
        self._touch_1_active.value = not (in_report.touch_1_0 & 0x80)
        self._touch_1_id.value = (in_report.touch_1_0 & 0x7F)
        self._touch_1_x.value = ((in_report.touch_1_2 & 0x0F) << 8) | in_report.touch_1_1
        self._touch_1_y.value = (in_report.touch_1_3 << 4) | ((in_report.touch_1_2 & 0xF0) >> 4)

        # ##### TRIGGER FEEDBACK #####
        self._l2_feedback_active.value = bool(in_report.l2_feedback & 0x10)
        self._l2_feedback_value.value = in_report.l2_feedback & 0xff
        self._r2_feedback_active.value = bool(in_report.r2_feedback & 0x10)
        self._r2_feedback_value.value = in_report.r2_feedback & 0xff

        # ##### BATTERY #####
        batt_level_raw: int = in_report.battery_0 & 0x0f
        if batt_level_raw > 8:
            batt_level_raw = 8
        batt_level: float = batt_level_raw / 8
        self._battery_level_percent.value = batt_level * 100
        self._battery_full.value = not not (in_report.battery_0 & 0x20)
        self._battery_charging.value = not not (in_report.battery_1 & 0x08)

    @property
    def left_stick_x(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._left_stick_x)

    @property
    def left_stick_y(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._left_stick_y)

    @property
    def right_stick_x(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._right_stick_x)

    @property
    def right_stick_y(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._right_stick_y)

    @property
    def l2(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._l2)

    @property
    def r2(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._r2)

    @property
    def btn_up(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_up)

    @property
    def btn_left(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_left)

    @property
    def btn_down(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_down)

    @property
    def btn_right(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_right)

    @property
    def btn_square(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_square)

    @property
    def btn_cross(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_cross)

    @property
    def btn_circle(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_circle)

    @property
    def btn_triangle(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_triangle)

    @property
    def btn_l1(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_l1)

    @property
    def btn_r1(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_r1)

    @property
    def btn_l2(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_l2)

    @property
    def btn_r2(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_r2)

    @property
    def btn_create(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_create)

    @property
    def btn_options(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_options)

    @property
    def btn_l3(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_l3)

    @property
    def btn_r3(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_r3)

    @property
    def btn_ps(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_ps)

    @property
    def btn_touchpad(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_touchpad)

    @property
    def btn_mute(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._btn_mute)

    @property
    def gyroscope_x(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._gyroscope_x)

    @property
    def gyroscope_y(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._gyroscope_y)

    @property
    def gyroscope_z(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._gyroscope_z)

    @property
    def accelerometer_x(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._accelerometer_x)

    @property
    def accelerometer_y(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._accelerometer_y)

    @property
    def accelerometer_z(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._accelerometer_z)

    @property
    def touch_0_active(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._touch_0_active)

    @property
    def touch_0_id(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._touch_0_id)

    @property
    def touch_0_x(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._touch_0_x)

    @property
    def touch_0_y(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._touch_0_y)

    @property
    def touch_1_active(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._touch_1_active)

    @property
    def touch_1_id(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._touch_1_id)

    @property
    def touch_1_x(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._touch_1_x)

    @property
    def touch_1_y(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._touch_1_y)

    @property
    def l2_feedback_active(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._l2_feedback_active)

    @property
    def l2_feedback_value(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._l2_feedback_value)

    @property
    def r2_feedback_active(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._r2_feedback_active)

    @property
    def r2_feedback_value(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._r2_feedback_value)

    @property
    def battery_level_percent(self) -> _StatePublicAccess[float]:
        return _StatePublicAccess(self._battery_level_percent)

    @property
    def battery_full(self) -> _StatePublicAccess[bool]:
        return _StatePublicAccess(self._battery_full)

    @property
    def battery_charging(self) -> _StatePublicAccess[int]:
        return _StatePublicAccess(self._battery_charging)
