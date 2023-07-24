from typing import Final

from dualsense_controller import State, BaseStates, RestrictedStateAccess
from dualsense_controller.common import (
    ReadStateName,
    StateChangeCallback,
    AnyStateChangeCallback,
    ConnectionType,
    Accelerometer,
    Gyroscope,
    StateValueMapping,
    JoyStick,
    Orientation
)
from dualsense_controller.reports import InReport


class ReadStates(BaseStates[ReadStateName]):

    def __init__(
            self,
            analog_threshold: int = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            state_value_mapping: StateValueMapping = StateValueMapping.DEFAULT,
    ):
        super().__init__()
        self._analog_threshold: int = analog_threshold
        self._gyroscope_threshold: int = gyroscope_threshold
        self._accelerometer_threshold: int = accelerometer_threshold
        self._state_value_mapping: StateValueMapping = state_value_mapping

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
        # COMPLEX
        self._left_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK
        )
        self._right_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK
        )
        self._gyroscope: Final[State[Gyroscope]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE
        )
        self._accelerometer: Final[State[Accelerometer]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER
        )
        self._orientation: Final[State[Orientation]] = self._create_and_register_state(
            ReadStateName.ORIENTATION
        )

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
        left_stick_x: int = in_report.axes_0
        left_stick_y: int = in_report.axes_1
        self._left_stick_x.value = left_stick_x
        self._left_stick_y.value = left_stick_y
        if self._left_stick_x.changed or self._left_stick_y.changed:
            self._left_stick.value = JoyStick(
                x=left_stick_x,
                y=left_stick_y
            )

        right_stick_x: int = in_report.axes_2
        right_stick_y: int = in_report.axes_3
        self._right_stick_x.value = right_stick_x
        self._right_stick_y.value = right_stick_y
        if self._right_stick_x.changed or self._right_stick_y.changed:
            self._right_stick.value = JoyStick(
                x=right_stick_x,
                y=right_stick_y
            )

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

        if self._gyroscope_x.changed or self._gyroscope_y.changed or self._gyroscope_z.changed:
            self._gyroscope.value = Gyroscope(
                x=gyro_x,
                y=gyro_y,
                z=gyro_z,
            )

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

        if self._accelerometer_x.changed or self._accelerometer_y.changed or self._accelerometer_z.changed:
            self._accelerometer.value = Accelerometer(
                x=accel_x,
                y=accel_y,
                z=accel_z,
            )

        if self._accelerometer.changed or self._gyroscope.changed:
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
