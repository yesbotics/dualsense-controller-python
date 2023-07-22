from typing import Type

from dualsense_controller import State
from dualsense_controller.common import ReadStateName, StateChangeCallback, AnyStateChangeCallback, ConnectionType
from dualsense_controller.reports import InReport


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
        self._states_dict: dict[ReadStateName, State] = {}

        self._create_state(ReadStateName.LEFT_STICK_X, int, threshold=analog_threshold)
        self._create_state(ReadStateName.LEFT_STICK_Y, int, threshold=analog_threshold)
        self._create_state(ReadStateName.RIGHT_STICK_X, int, threshold=analog_threshold)
        self._create_state(ReadStateName.RIGHT_STICK_Y, int, threshold=analog_threshold)
        self._create_state(ReadStateName.L2, int, threshold=analog_threshold)
        self._create_state(ReadStateName.R2, int, threshold=analog_threshold)
        self._create_state(ReadStateName.BTN_UP, bool)
        self._create_state(ReadStateName.BTN_LEFT, bool)
        self._create_state(ReadStateName.BTN_DOWN, bool)
        self._create_state(ReadStateName.BTN_RIGHT, bool)
        self._create_state(ReadStateName.BTN_SQUARE, bool)
        self._create_state(ReadStateName.BTN_CROSS, bool)
        self._create_state(ReadStateName.BTN_CIRCLE, bool)
        self._create_state(ReadStateName.BTN_TRIANGLE, bool)
        self._create_state(ReadStateName.BTN_L1, bool)
        self._create_state(ReadStateName.BTN_R1, bool)
        self._create_state(ReadStateName.BTN_L2, bool)
        self._create_state(ReadStateName.BTN_R2, bool)
        self._create_state(ReadStateName.BTN_CREATE, bool)
        self._create_state(ReadStateName.BTN_OPTIONS, bool)
        self._create_state(ReadStateName.BTN_L3, bool)
        self._create_state(ReadStateName.BTN_R3, bool)
        self._create_state(ReadStateName.BTN_PS, bool)
        self._create_state(ReadStateName.BTN_TOUCHPAD, bool)
        self._create_state(ReadStateName.BTN_MUTE, bool)
        self._create_state(ReadStateName.GYROSCOPE_X, int, threshold=gyroscope_threshold)
        self._create_state(ReadStateName.GYROSCOPE_Y, int, threshold=gyroscope_threshold)
        self._create_state(ReadStateName.GYROSCOPE_Z, int, threshold=gyroscope_threshold)
        self._create_state(ReadStateName.ACCELEROMETER_X, int, threshold=accelerometer_threshold)
        self._create_state(ReadStateName.ACCELEROMETER_Y, int, threshold=accelerometer_threshold)
        self._create_state(ReadStateName.ACCELEROMETER_Z, int, threshold=accelerometer_threshold)
        self._create_state(ReadStateName.TOUCH_0_ACTIVE, bool)
        self._create_state(ReadStateName.TOUCH_0_ID, int)
        self._create_state(ReadStateName.TOUCH_0_X, int)
        self._create_state(ReadStateName.TOUCH_0_Y, int)
        self._create_state(ReadStateName.TOUCH_1_ACTIVE, bool)
        self._create_state(ReadStateName.TOUCH_1_ID, int)
        self._create_state(ReadStateName.TOUCH_1_X, int)
        self._create_state(ReadStateName.TOUCH_1_Y, int)
        self._create_state(ReadStateName.L2_FEEDBACK_ACTIVE, bool)
        self._create_state(ReadStateName.L2_FEEDBACK_VALUE, int)
        self._create_state(ReadStateName.R2_FEEDBACK_ACTIVE, bool)
        self._create_state(ReadStateName.R2_FEEDBACK_VALUE, int)
        self._create_state(ReadStateName.BATTERY_LEVEL_PERCENT, float, skip_none=False)
        self._create_state(ReadStateName.BATTERY_FULL, bool, skip_none=False)
        self._create_state(ReadStateName.BATTERY_CHARGING, int, skip_none=False)

    @property
    def states_dict(self) -> dict[ReadStateName, State]:
        return self._states_dict

    @property
    def analog_threshold(self) -> int:
        return self._analog_threshold

    @analog_threshold.setter
    def analog_threshold(self, analog_threshold: int) -> None:
        self._analog_threshold = analog_threshold
        self._get_state(ReadStateName.LEFT_STICK_X).threshold = analog_threshold
        self._get_state(ReadStateName.LEFT_STICK_Y).threshold = analog_threshold
        self._get_state(ReadStateName.RIGHT_STICK_X).threshold = analog_threshold
        self._get_state(ReadStateName.RIGHT_STICK_Y).threshold = analog_threshold
        self._get_state(ReadStateName.L2).threshold = analog_threshold
        self._get_state(ReadStateName.R2).threshold = analog_threshold

    @property
    def accelerometer_threshold(self) -> int:
        return self._accelerometer_threshold

    @accelerometer_threshold.setter
    def accelerometer_threshold(self, accelerometer_threshold: int) -> None:
        self._accelerometer_threshold = accelerometer_threshold
        self._get_state(ReadStateName.ACCELEROMETER_X).threshold = accelerometer_threshold
        self._get_state(ReadStateName.ACCELEROMETER_Y).threshold = accelerometer_threshold
        self._get_state(ReadStateName.ACCELEROMETER_Z).threshold = accelerometer_threshold

    @property
    def gyroscope_threshold(self) -> int:
        return self._gyroscope_threshold

    @gyroscope_threshold.setter
    def gyroscope_threshold(self, gyroscope_threshold: int) -> None:
        self._gyroscope_threshold = gyroscope_threshold
        self._get_state(ReadStateName.GYROSCOPE_X).threshold = gyroscope_threshold
        self._get_state(ReadStateName.GYROSCOPE_Y).threshold = gyroscope_threshold
        self._get_state(ReadStateName.GYROSCOPE_Z).threshold = gyroscope_threshold

    def on_change(self, name: ReadStateName, callback: StateChangeCallback):
        self._get_state(name).on_change(lambda _, old_value, new_value: callback(old_value, new_value))

    def on_change_any(self, callback: AnyStateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.on_change(callback)

    def _create_state(self, name: ReadStateName, data_type: Type, threshold: int = 0, skip_none: False = True) -> None:
        self._states_dict[name] = State[data_type](name, threshold=threshold, skip_none=skip_none)

    def _get_state(self, name: ReadStateName) -> State:
        return self._states_dict[name]

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        # ##### ANALOG STICKS #####
        self._get_state(ReadStateName.LEFT_STICK_X).value = in_report.axes_0
        self._get_state(ReadStateName.LEFT_STICK_Y).value = in_report.axes_1
        self._get_state(ReadStateName.RIGHT_STICK_X).value = in_report.axes_2
        self._get_state(ReadStateName.RIGHT_STICK_Y).value = in_report.axes_3
        self._get_state(ReadStateName.L2).value = in_report.axes_4
        self._get_state(ReadStateName.R2).value = in_report.axes_5

        # ##### BUTTONS #####
        dpad: int = in_report.buttons_0 & 0x0f
        self._get_state(ReadStateName.BTN_UP).value = dpad == 0 or dpad == 1 or dpad == 7
        self._get_state(ReadStateName.BTN_DOWN).value = dpad == 3 or dpad == 4 or dpad == 5
        self._get_state(ReadStateName.BTN_LEFT).value = dpad == 5 or dpad == 6 or dpad == 7
        self._get_state(ReadStateName.BTN_RIGHT).value = dpad == 1 or dpad == 2 or dpad == 3
        self._get_state(ReadStateName.BTN_SQUARE).value = bool(in_report.buttons_0 & 0x10)
        self._get_state(ReadStateName.BTN_CROSS).value = bool(in_report.buttons_0 & 0x20)
        self._get_state(ReadStateName.BTN_CIRCLE).value = bool(in_report.buttons_0 & 0x40)
        self._get_state(ReadStateName.BTN_TRIANGLE).value = bool(in_report.buttons_0 & 0x80)
        self._get_state(ReadStateName.BTN_L1).value = bool(in_report.buttons_1 & 0x01)
        self._get_state(ReadStateName.BTN_R1).value = bool(in_report.buttons_1 & 0x02)
        self._get_state(ReadStateName.BTN_L2).value = bool(in_report.buttons_1 & 0x04)
        self._get_state(ReadStateName.BTN_R2).value = bool(in_report.buttons_1 & 0x08)
        self._get_state(ReadStateName.BTN_CREATE).value = bool(in_report.buttons_1 & 0x10)
        self._get_state(ReadStateName.BTN_OPTIONS).value = bool(in_report.buttons_1 & 0x20)
        self._get_state(ReadStateName.BTN_L3).value = bool(in_report.buttons_1 & 0x40)
        self._get_state(ReadStateName.BTN_R3).value = bool(in_report.buttons_1 & 0x80)
        self._get_state(ReadStateName.BTN_PS).value = bool(in_report.buttons_2 & 0x01)
        self._get_state(ReadStateName.BTN_TOUCHPAD).value = bool(in_report.buttons_2 & 0x02)
        self._get_state(ReadStateName.BTN_MUTE).value = bool(in_report.buttons_2 & 0x04)

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
        self._get_state(ReadStateName.GYROSCOPE_X).value = gyro_x
        self._get_state(ReadStateName.GYROSCOPE_Y).value = gyro_y
        self._get_state(ReadStateName.GYROSCOPE_Z).value = gyro_z

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
        self._get_state(ReadStateName.ACCELEROMETER_X).value = accel_x
        self._get_state(ReadStateName.ACCELEROMETER_Y).value = accel_y
        self._get_state(ReadStateName.ACCELEROMETER_Z).value = accel_z

        # ##### TOUCH #####
        self._get_state(ReadStateName.TOUCH_0_ACTIVE).value = not (in_report.touch_0_0 & 0x80)
        self._get_state(ReadStateName.TOUCH_0_ID).value = (in_report.touch_0_0 & 0x7F)
        self._get_state(ReadStateName.TOUCH_0_X).value = ((in_report.touch_0_2 & 0x0F) << 8) | in_report.touch_0_1
        self._get_state(ReadStateName.TOUCH_0_Y).value = (in_report.touch_0_3 << 4) | (
                (in_report.touch_0_2 & 0xF0) >> 4)
        self._get_state(ReadStateName.TOUCH_1_ACTIVE).value = not (in_report.touch_1_0 & 0x80)
        self._get_state(ReadStateName.TOUCH_1_ID).value = (in_report.touch_1_0 & 0x7F)
        self._get_state(ReadStateName.TOUCH_1_X).value = ((in_report.touch_1_2 & 0x0F) << 8) | in_report.touch_1_1
        self._get_state(ReadStateName.TOUCH_1_Y).value = (in_report.touch_1_3 << 4) | (
                (in_report.touch_1_2 & 0xF0) >> 4)

        # ##### TRIGGER FEEDBACK #####
        self._get_state(ReadStateName.L2_FEEDBACK_ACTIVE).value = bool(in_report.l2_feedback & 0x10)
        self._get_state(ReadStateName.L2_FEEDBACK_VALUE).value = in_report.l2_feedback & 0xff
        self._get_state(ReadStateName.R2_FEEDBACK_ACTIVE).value = bool(in_report.r2_feedback & 0x10)
        self._get_state(ReadStateName.R2_FEEDBACK_VALUE).value = in_report.r2_feedback & 0xff

        # ##### BATTERY #####
        self._get_state(ReadStateName.BATTERY_LEVEL_PERCENT).value = (in_report.battery_0 & 0x0f) * 100 / 8
        self._get_state(ReadStateName.BATTERY_FULL).value = not not (in_report.battery_0 & 0x20)
        self._get_state(ReadStateName.BATTERY_CHARGING).value = not not (in_report.battery_1 & 0x08)
