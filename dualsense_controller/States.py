from typing import Final

import pyee

from dualsense_controller import StateName, ValueType, State


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

    def update(self, report: bytes) -> None:
        # ##### ANALOG STICKS #####
        left_stick_x: int = report[0]
        left_stick_y: int = report[1]
        right_stick_x: int = report[2]
        right_stick_y: int = report[3]
        l2: int = report[4]
        r2: int = report[5]
        self._left_stick_x.value = left_stick_x
        self._left_stick_y.value = left_stick_y
        self._right_stick_x.value = right_stick_x
        self._right_stick_y.value = right_stick_y
        self._l2.value = l2
        self._r2.value = r2

        # ##### WHATEVER #####
        # seqNum:int = report[6]

        # ##### BUTTONS #####
        buttons0: int = report[7]
        buttons1: int = report[8]
        buttons2: int = report[9]
        # buttons3: int = report[10]
        dpad: int = buttons0 & 0x0f
        self._btn_up.value = dpad == 0 or dpad == 1 or dpad == 7
        self._btn_down.value = dpad == 3 or dpad == 4 or dpad == 5
        self._btn_left.value = dpad == 5 or dpad == 6 or dpad == 7
        self._btn_right.value = dpad == 1 or dpad == 2 or dpad == 3
        self._btn_square.value = bool(buttons0 & 0x10)
        self._btn_cross.value = bool(buttons0 & 0x20)
        self._btn_circle.value = bool(buttons0 & 0x40)
        self._btn_triangle.value = bool(buttons0 & 0x80)
        self._btn_l1.value = bool(buttons1 & 0x01)
        self._btn_r1.value = bool(buttons1 & 0x02)
        self._btn_l2.value = bool(buttons1 & 0x04)
        self._btn_r2.value = bool(buttons1 & 0x08)
        self._btn_create.value = bool(buttons1 & 0x10)
        self._btn_options.value = bool(buttons1 & 0x20)
        self._btn_l3.value = bool(buttons1 & 0x40)
        self._btn_r3.value = bool(buttons1 & 0x80)
        self._btn_ps.value = bool(buttons2 & 0x01)
        self._btn_touchpad.value = bool(buttons2 & 0x02)
        self._btn_mute.value = bool(buttons2 & 0x04)

        # ##### WHATEVER #####
        timestamp0: int = report[11]
        timestamp1: int = report[12]
        timestamp2: int = report[13]
        timestamp3: int = report[14]

        # ##### GYRO #####
        gyro_x0: int = report[15]
        gyro_x1: int = report[16]
        gyro_y0: int = report[17]
        gyro_y1: int = report[18]
        gyro_z0: int = report[19]
        gyro_z1: int = report[20]
        gyro_x: int = (gyro_x1 << 8) | gyro_x0
        if gyro_x > 0x7FFF:
            gyro_x -= 0x10000
        gyro_y: int = (gyro_y1 << 8) | gyro_y0
        if gyro_y > 0x7FFF:
            gyro_y -= 0x10000
        gyro_z: int = (gyro_z1 << 8) | gyro_z0
        if gyro_z > 0x7FFF:
            gyro_z -= 0x10000
        self._gyroscope_x.value = gyro_x
        self._gyroscope_y.value = gyro_y
        self._gyroscope_z.value = gyro_z

        # ##### ACCEL #####
        accel_x0: int = report[21]
        accel_x1: int = report[22]
        accel_y0: int = report[23]
        accel_y1: int = report[24]
        accel_z0: int = report[25]
        accel_z1: int = report[26]
        accel_x: int = (accel_x1 << 8) | accel_x0
        if accel_x > 0x7FFF:
            accel_x -= 0x10000
        accel_y: int = (accel_y1 << 8) | accel_y0
        if accel_y > 0x7FFF:
            accel_y -= 0x10000
        accel_z: int = (accel_z1 << 8) | accel_z0
        if accel_z > 0x7FFF:
            accel_z -= 0x10000
        self._accelerometer_x.value = accel_x
        self._accelerometer_y.value = accel_y
        self._accelerometer_z.value = accel_z

        # ##### WHATEVER #####
        # sensorTimestamp0: int = report[27]
        # sensorTimestamp1: int = report[28]
        # sensorTimestamp2: int = report[29]
        # sensorTimestamp3: int = report[30]
        # ??? = report[31]

        # ##### TOUCH #####
        touch_00: int = report[32]
        touch_01: int = report[33]
        touch_02: int = report[34]
        touch_03: int = report[35]
        touch_10: int = report[36]
        touch_11: int = report[37]
        touch_12: int = report[38]
        touch_13: int = report[39]

        self._touch_0_active.value = not (touch_00 & 0x80)
        self._touch_0_id.value = (touch_00 & 0x7F)
        self._touch_0_x.value = ((touch_02 & 0x0F) << 8) | touch_01
        self._touch_0_y.value = (touch_03 << 4) | ((touch_02 & 0xF0) >> 4)
        self._touch_1_active.value = not (touch_10 & 0x80)
        self._touch_1_id.value = (touch_10 & 0x7F)
        self._touch_1_x.value = ((touch_12 & 0x0F) << 8) | touch_11
        self._touch_1_y.value = (touch_13 << 4) | ((touch_12 & 0xF0) >> 4)

        # ##### WHATEVER #####
        # ??? = report[40]

        # ##### TRIGGER FEEDBACK #####
        r2_feedback: int = report[41]
        l2_feedback: int = report[42]
        self._l2_feedback_active.value = bool(l2_feedback & 0x10)
        self._l2_feedback_value.value = l2_feedback & 0xff
        self._r2_feedback_active.value = bool(r2_feedback & 0x10)
        self._r2_feedback_value.value = r2_feedback & 0xff

        # ##### WHATEVER #####
        # ??? = report[43:52] bytes 43-51

        # ##### BATTERY #####
        battery0: int = report[52]
        battery1: int = report[53]
        self._battery_level_percent.value = (battery0 & 0x0f) * 100 / 8
        self._battery_full.value = not not (battery0 & 0x20)
        self._battery_charging.value = not not (battery1 & 0x08)

        # ##### WHATEVER #####
        # ??? = report[54:59] bytes 54-58
        # ??? = report[59:63] bytes 59-62 CRC32 checksum
