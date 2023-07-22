from typing import Final

import pyee

from dualsense_controller import StateName, ValueType, State, ConnectionType, InReport


class States(pyee.EventEmitter):
    EVENT_CHANGE: Final[str] = 'change'

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

        self._left_stick_x: State[int] = State[int](StateName.LEFT_STICK_X, threshold=analog_threshold)
        self._left_stick_y: State[int] = State[int](StateName.LEFT_STICK_Y, threshold=analog_threshold)
        self._right_stick_x: State[int] = State[int](StateName.RIGHT_STICK_X, threshold=analog_threshold)
        self._right_stick_y: State[int] = State[int](StateName.RIGHT_STICK_Y, threshold=analog_threshold)
        self._l2: State[int] = State[int](StateName.L2, threshold=analog_threshold)
        self._r2: State[int] = State[int](StateName.R2, threshold=analog_threshold)
        self._btn_up: State[bool] = State[bool](StateName.BTN_UP)
        self._btn_left: State[bool] = State[bool](StateName.BTN_LEFT)
        self._btn_down: State[bool] = State[bool](StateName.BTN_DOWN)
        self._btn_right: State[bool] = State[bool](StateName.BTN_RIGHT)
        self._btn_square: State[bool] = State[bool](StateName.BTN_SQUARE)
        self._btn_cross: State[bool] = State[bool](StateName.BTN_CROSS)
        self._btn_circle: State[bool] = State[bool](StateName.BTN_CIRCLE)
        self._btn_triangle: State[bool] = State[bool](StateName.BTN_TRIANGLE)
        self._btn_l1: State[bool] = State[bool](StateName.BTN_L1)
        self._btn_r1: State[bool] = State[bool](StateName.BTN_R1)
        self._btn_l2: State[bool] = State[bool](StateName.BTN_L2)
        self._btn_r2: State[bool] = State[bool](StateName.BTN_R2)
        self._btn_create: State[bool] = State[bool](StateName.BTN_CREATE)
        self._btn_options: State[bool] = State[bool](StateName.BTN_OPTIONS)
        self._btn_l3: State[bool] = State[bool](StateName.BTN_L3)
        self._btn_r3: State[bool] = State[bool](StateName.BTN_R3)
        self._btn_ps: State[bool] = State[bool](StateName.BTN_PS)
        self._btn_touchpad: State[bool] = State[bool](StateName.BTN_TOUCHPAD)
        self._btn_mute: State[bool] = State[bool](StateName.BTN_MUTE)
        self._gyroscope_x: State[int] = State[int](StateName.GYROSCOPE_X, threshold=gyroscope_threshold)
        self._gyroscope_y: State[int] = State[int](StateName.GYROSCOPE_Y, threshold=gyroscope_threshold)
        self._gyroscope_z: State[int] = State[int](StateName.GYROSCOPE_Z, threshold=gyroscope_threshold)
        self._accelerometer_x: State[int] = State[int](StateName.ACCELEROMETER_X, threshold=accelerometer_threshold)
        self._accelerometer_y: State[int] = State[int](StateName.ACCELEROMETER_Y, threshold=accelerometer_threshold)
        self._accelerometer_z: State[int] = State[int](StateName.ACCELEROMETER_Z, threshold=accelerometer_threshold)
        self._touch_0_active: State[bool] = State[bool](StateName.TOUCH_0_ACTIVE)
        self._touch_0_id: State[int] = State[int](StateName.TOUCH_0_ID)
        self._touch_0_x: State[int] = State[int](StateName.TOUCH_0_X)
        self._touch_0_y: State[int] = State[int](StateName.TOUCH_0_Y)
        self._touch_1_active: State[bool] = State[bool](StateName.TOUCH_1_ACTIVE)
        self._touch_1_id: State[int] = State[int](StateName.TOUCH_1_ID)
        self._touch_1_x: State[int] = State[int](StateName.TOUCH_1_X)
        self._touch_1_y: State[int] = State[int](StateName.TOUCH_1_Y)
        self._l2_feedback_active: State[bool] = State[bool](StateName.L2_FEEDBACK_ACTIVE)
        self._l2_feedback_value: State[int] = State[int](StateName.L2_FEEDBACK_VALUE)
        self._r2_feedback_active: State[bool] = State[bool](StateName.R2_FEEDBACK_ACTIVE)
        self._r2_feedback_value: State[int] = State[int](StateName.R2_FEEDBACK_VALUE)
        self._battery_level_percent: State[float] = State[float](StateName.BATTERY_LEVEL_PERCENT, skip_none=False)
        self._battery_full: State[bool] = State[bool](StateName.BATTERY_FULL, skip_none=False)
        self._battery_charging: State[int] = State[int](StateName.BATTERY_CHARGING, skip_none=False)

        self._left_stick_x.on(State.EVENT_CHANGE, self._on_change)
        self._left_stick_y.on(State.EVENT_CHANGE, self._on_change)
        self._right_stick_x.on(State.EVENT_CHANGE, self._on_change)
        self._right_stick_y.on(State.EVENT_CHANGE, self._on_change)
        self._l2.on(State.EVENT_CHANGE, self._on_change)
        self._r2.on(State.EVENT_CHANGE, self._on_change)
        self._btn_up.on(State.EVENT_CHANGE, self._on_change)
        self._btn_left.on(State.EVENT_CHANGE, self._on_change)
        self._btn_down.on(State.EVENT_CHANGE, self._on_change)
        self._btn_right.on(State.EVENT_CHANGE, self._on_change)
        self._btn_square.on(State.EVENT_CHANGE, self._on_change)
        self._btn_cross.on(State.EVENT_CHANGE, self._on_change)
        self._btn_circle.on(State.EVENT_CHANGE, self._on_change)
        self._btn_triangle.on(State.EVENT_CHANGE, self._on_change)
        self._btn_l1.on(State.EVENT_CHANGE, self._on_change)
        self._btn_r1.on(State.EVENT_CHANGE, self._on_change)
        self._btn_l2.on(State.EVENT_CHANGE, self._on_change)
        self._btn_r2.on(State.EVENT_CHANGE, self._on_change)
        self._btn_create.on(State.EVENT_CHANGE, self._on_change)
        self._btn_options.on(State.EVENT_CHANGE, self._on_change)
        self._btn_l3.on(State.EVENT_CHANGE, self._on_change)
        self._btn_r3.on(State.EVENT_CHANGE, self._on_change)
        self._btn_ps.on(State.EVENT_CHANGE, self._on_change)
        self._btn_touchpad.on(State.EVENT_CHANGE, self._on_change)
        self._btn_mute.on(State.EVENT_CHANGE, self._on_change)
        self._gyroscope_x.on(State.EVENT_CHANGE, self._on_change)
        self._gyroscope_y.on(State.EVENT_CHANGE, self._on_change)
        self._gyroscope_z.on(State.EVENT_CHANGE, self._on_change)
        self._accelerometer_x.on(State.EVENT_CHANGE, self._on_change)
        self._accelerometer_y.on(State.EVENT_CHANGE, self._on_change)
        self._accelerometer_z.on(State.EVENT_CHANGE, self._on_change)
        self._touch_0_active.on(State.EVENT_CHANGE, self._on_change)
        self._touch_0_id.on(State.EVENT_CHANGE, self._on_change)
        self._touch_0_x.on(State.EVENT_CHANGE, self._on_change)
        self._touch_0_y.on(State.EVENT_CHANGE, self._on_change)
        self._touch_1_active.on(State.EVENT_CHANGE, self._on_change)
        self._touch_1_id.on(State.EVENT_CHANGE, self._on_change)
        self._touch_1_x.on(State.EVENT_CHANGE, self._on_change)
        self._touch_1_y.on(State.EVENT_CHANGE, self._on_change)
        self._l2_feedback_active.on(State.EVENT_CHANGE, self._on_change)
        self._l2_feedback_value.on(State.EVENT_CHANGE, self._on_change)
        self._r2_feedback_active.on(State.EVENT_CHANGE, self._on_change)
        self._r2_feedback_value.on(State.EVENT_CHANGE, self._on_change)
        self._battery_level_percent.on(State.EVENT_CHANGE, self._on_change)
        self._battery_full.on(State.EVENT_CHANGE, self._on_change)
        self._battery_charging.on(State.EVENT_CHANGE, self._on_change)

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

    def _on_change(self, name: StateName, old_value: ValueType, new_value: ValueType) -> None:
        self.emit(States.EVENT_CHANGE, name, old_value, new_value)

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
        self._gyroscope_x.value = gyro_x
        gyro_y: int = (in_report.gyro_y_1 << 8) | in_report.gyro_y_0
        if gyro_y > 0x7FFF:
            gyro_y -= 0x10000
        self._gyroscope_y.value = gyro_y
        gyro_z: int = (in_report.gyro_z_1 << 8) | in_report.gyro_z_0
        if gyro_z > 0x7FFF:
            gyro_z -= 0x10000
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
        self._battery_level_percent.value = (in_report.battery_0 & 0x0f) * 100 / 8
        self._battery_full.value = not not (in_report.battery_0 & 0x20)
        self._battery_charging.value = not not (in_report.battery_1 & 0x08)
