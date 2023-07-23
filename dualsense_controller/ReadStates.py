from __future__ import annotations

from typing import Final, TypeVar

from dualsense_controller import State
from dualsense_controller.common import ReadStateName, StateChangeCallback, AnyStateChangeCallback, ConnectionType
from dualsense_controller.reports import InReport

_StateType = TypeVar('_StateType')


class ReadStates:

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
        self._states_dict: Final[dict[ReadStateName, State]] = {}

        self.left_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X, int, threshold=analog_threshold
        )
        self.left_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y, int, threshold=analog_threshold
        )
        self.right_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X, int, threshold=analog_threshold
        )
        self.right_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y, int, threshold=analog_threshold
        )
        self.l2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2, int, threshold=analog_threshold
        )
        self.r2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2, int, threshold=analog_threshold
        )
        self.btn_up: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_UP, bool
        )
        self.btn_left: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_LEFT, bool
        )
        self.btn_down: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_DOWN, bool
        )
        self.btn_right: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_RIGHT, bool
        )
        self.btn_square: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_SQUARE, bool
        )
        self.btn_cross: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CROSS, bool
        )
        self.btn_circle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CIRCLE, bool
        )
        self.btn_triangle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TRIANGLE, bool
        )
        self.btn_l1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L1, bool
        )
        self.btn_r1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R1, bool
        )
        self.btn_l2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L2, bool
        )
        self.btn_r2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R2, bool
        )
        self.btn_create: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CREATE, bool
        )
        self.btn_options: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_OPTIONS, bool
        )
        self.btn_l3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L3, bool
        )
        self.btn_r3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R3, bool
        )
        self.btn_ps: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_PS, bool
        )
        self.btn_touchpad: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TOUCHPAD, bool
        )
        self.btn_mute: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_MUTE, bool
        )
        self.gyroscope_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_X, int, threshold=gyroscope_threshold
        )
        self.gyroscope_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Y, int, threshold=gyroscope_threshold
        )
        self.gyroscope_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Z, int, threshold=gyroscope_threshold
        )
        self.accelerometer_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_X, int, threshold=accelerometer_threshold
        )
        self.accelerometer_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Y, int, threshold=accelerometer_threshold
        )
        self.accelerometer_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Z, int, threshold=accelerometer_threshold
        )
        self.touch_0_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ACTIVE, bool
        )
        self.touch_0_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ID, int
        )
        self.touch_0_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_X, int
        )
        self.touch_0_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_Y, int
        )
        self.touch_1_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ACTIVE, bool
        )
        self.touch_1_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ID, int
        )
        self.touch_1_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_X, int
        )
        self.touch_1_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_Y, int
        )
        self.l2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_ACTIVE, bool
        )
        self.l2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_VALUE, int
        )
        self.r2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_ACTIVE, bool
        )
        self.r2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_VALUE, int
        )
        self.battery_level_percent: Final[State[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT, float, skip_none=False
        )
        self.battery_full: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL, bool, skip_none=False
        )
        self.battery_charging: Final[State[int]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING, int, skip_none=False
        )

    @property
    def analog_threshold(self) -> int:
        return self._analog_threshold

    @analog_threshold.setter
    def analog_threshold(self, analog_threshold: int) -> None:
        self._analog_threshold = analog_threshold
        self.left_stick_x.threshold = analog_threshold
        self.left_stick_y.threshold = analog_threshold
        self.right_stick_x.threshold = analog_threshold
        self.right_stick_y.threshold = analog_threshold
        self.l2.threshold = analog_threshold
        self.r2.threshold = analog_threshold

    @property
    def accelerometer_threshold(self) -> int:
        return self._accelerometer_threshold

    @accelerometer_threshold.setter
    def accelerometer_threshold(self, accelerometer_threshold: int) -> None:
        self._accelerometer_threshold = accelerometer_threshold
        self.accelerometer_x.threshold = accelerometer_threshold
        self.accelerometer_y.threshold = accelerometer_threshold
        self.accelerometer_z.threshold = accelerometer_threshold

    @property
    def gyroscope_threshold(self) -> int:
        return self._gyroscope_threshold

    @gyroscope_threshold.setter
    def gyroscope_threshold(self, gyroscope_threshold: int) -> None:
        self._gyroscope_threshold = gyroscope_threshold
        self.gyroscope_x.threshold = gyroscope_threshold
        self.gyroscope_y.threshold = gyroscope_threshold
        self.gyroscope_z.threshold = gyroscope_threshold

    def on_change(self, name_or_callback: ReadStateName | AnyStateChangeCallback, callback: StateChangeCallback = None):
        if callback is None:
            self.on_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).on_change(callback)

    def on_any_change(self, callback: AnyStateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.on_change(lambda old_value, new_value: callback(state_name, old_value, new_value))

    def _create_and_register_state(
            self,
            name: ReadStateName,
            data_type: _StateType,
            threshold: int = 0,
            skip_none: False = True
    ) -> State:
        state: State[_StateType] = State[data_type](name, threshold=threshold, skip_none=skip_none)
        self._states_dict[name] = state
        return state

    def _get_state_by_name(self, name: ReadStateName) -> State:
        return self._states_dict[name]

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        # ##### ANALOG STICKS #####
        self.left_stick_x.value = in_report.axes_0
        self.left_stick_y.value = in_report.axes_1
        self.right_stick_x.value = in_report.axes_2
        self.right_stick_y.value = in_report.axes_3
        self.l2.value = in_report.axes_4
        self.r2.value = in_report.axes_5

        # ##### BUTTONS #####
        dpad: int = in_report.buttons_0 & 0x0f
        self.btn_up.value = dpad == 0 or dpad == 1 or dpad == 7
        self.btn_down.value = dpad == 3 or dpad == 4 or dpad == 5
        self.btn_left.value = dpad == 5 or dpad == 6 or dpad == 7
        self.btn_right.value = dpad == 1 or dpad == 2 or dpad == 3
        self.btn_square.value = bool(in_report.buttons_0 & 0x10)
        self.btn_cross.value = bool(in_report.buttons_0 & 0x20)
        self.btn_circle.value = bool(in_report.buttons_0 & 0x40)
        self.btn_triangle.value = bool(in_report.buttons_0 & 0x80)
        self.btn_l1.value = bool(in_report.buttons_1 & 0x01)
        self.btn_r1.value = bool(in_report.buttons_1 & 0x02)
        self.btn_l2.value = bool(in_report.buttons_1 & 0x04)
        self.btn_r2.value = bool(in_report.buttons_1 & 0x08)
        self.btn_create.value = bool(in_report.buttons_1 & 0x10)
        self.btn_options.value = bool(in_report.buttons_1 & 0x20)
        self.btn_l3.value = bool(in_report.buttons_1 & 0x40)
        self.btn_r3.value = bool(in_report.buttons_1 & 0x80)
        self.btn_ps.value = bool(in_report.buttons_2 & 0x01)
        self.btn_touchpad.value = bool(in_report.buttons_2 & 0x02)
        self.btn_mute.value = bool(in_report.buttons_2 & 0x04)

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
        self.gyroscope_x.value = gyro_x
        self.gyroscope_y.value = gyro_y
        self.gyroscope_z.value = gyro_z

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
        self.accelerometer_x.value = accel_x
        self.accelerometer_y.value = accel_y
        self.accelerometer_z.value = accel_z

        # ##### TOUCH #####
        self.touch_0_active.value = not (in_report.touch_0_0 & 0x80)
        self.touch_0_id.value = (in_report.touch_0_0 & 0x7F)
        self.touch_0_x.value = ((in_report.touch_0_2 & 0x0F) << 8) | in_report.touch_0_1
        self.touch_0_y.value = (in_report.touch_0_3 << 4) | ((in_report.touch_0_2 & 0xF0) >> 4)
        self.touch_1_active.value = not (in_report.touch_1_0 & 0x80)
        self.touch_1_id.value = (in_report.touch_1_0 & 0x7F)
        self.touch_1_x.value = ((in_report.touch_1_2 & 0x0F) << 8) | in_report.touch_1_1
        self.touch_1_y.value = (in_report.touch_1_3 << 4) | ((in_report.touch_1_2 & 0xF0) >> 4)

        # ##### TRIGGER FEEDBACK #####
        self.l2_feedback_active.value = bool(in_report.l2_feedback & 0x10)
        self.l2_feedback_value.value = in_report.l2_feedback & 0xff
        self.r2_feedback_active.value = bool(in_report.r2_feedback & 0x10)
        self.r2_feedback_value.value = in_report.r2_feedback & 0xff

        # ##### BATTERY #####
        self.battery_level_percent.value = (in_report.battery_0 & 0x0f) * 100 / 8
        self.battery_full.value = not not (in_report.battery_0 & 0x20)
        self.battery_charging.value = not not (in_report.battery_1 & 0x08)
