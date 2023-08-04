import math

from dualsense_controller.core.report.in_report import InReport
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Feedback, Gyroscope, JoyStick, \
    Orientation, \
    TouchFinger


class ValueCalc:

    def __init__(self):
        pass

    @classmethod
    def left_stick(cls, in_report: InReport) -> JoyStick:
        return JoyStick(x=in_report.axes_0, y=in_report.axes_1)

    @classmethod
    def left_stick_x(cls, _: InReport, left_stick: State[JoyStick]) -> int:
        return left_stick.value.x

    @classmethod
    def left_stick_y(cls, _: InReport, left_stick: State[JoyStick]) -> int:
        return left_stick.value.y

    @classmethod
    def right_stick(cls, in_report: InReport) -> JoyStick:
        return JoyStick(x=in_report.axes_2, y=in_report.axes_3)

    @classmethod
    def right_stick_x(cls, _: InReport, right_stick: State[JoyStick]) -> int:
        return right_stick.value.x

    @classmethod
    def right_stick_y(cls, _: InReport, right_stick: State[JoyStick]) -> int:
        return right_stick.value.y

    @classmethod
    def l2(cls, in_report: InReport) -> int:
        return in_report.axes_4

    @classmethod
    def r2(cls, in_report: InReport) -> int:
        return in_report.axes_5

    @classmethod
    def dpad(cls, in_report: InReport) -> int:
        return in_report.buttons_0 & 0x0f

    @classmethod
    def btn_up(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value == 0 or dpad.value == 1 or dpad.value == 7

    @classmethod
    def btn_down(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value == 3 or dpad.value == 4 or dpad.value == 5

    @classmethod
    def btn_left(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value == 5 or dpad.value == 6 or dpad.value == 7

    @classmethod
    def btn_right(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value == 1 or dpad.value == 2 or dpad.value == 3

    @classmethod
    def btn_cross(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x20)

    @classmethod
    def btn_r1(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x02)

    @classmethod
    def btn_square(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x10)

    @classmethod
    def btn_circle(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x40)

    @classmethod
    def btn_triangle(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x80)

    @classmethod
    def btn_l1(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x01)

    @classmethod
    def btn_l2(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x04)

    @classmethod
    def btn_r2(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x08)

    @classmethod
    def btn_create(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x10)

    @classmethod
    def btn_options(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x20)

    @classmethod
    def btn_l3(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x40)

    @classmethod
    def btn_r3(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x80)

    @classmethod
    def btn_ps(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_2 & 0x01)

    @classmethod
    def btn_mute(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_2 & 0x04)

    @classmethod
    def btn_touchpad(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_2 & 0x02)

    @classmethod
    def gyroscope(cls, in_report: InReport) -> Gyroscope:
        return Gyroscope(
            x=cls._sensor_axis(in_report.gyro_x_1, in_report.gyro_x_0),
            y=cls._sensor_axis(in_report.gyro_y_1, in_report.gyro_y_0),
            z=cls._sensor_axis(in_report.gyro_z_1, in_report.gyro_z_0),
        )

    @classmethod
    def gyroscope_x(cls, _: InReport, gyroscope: State[Gyroscope]) -> int:
        return gyroscope.value.x

    @classmethod
    def gyroscope_y(cls, _: InReport, gyroscope: State[Gyroscope]) -> int:
        return gyroscope.value.y

    @classmethod
    def gyroscope_z(cls, _: InReport, gyroscope: State[Gyroscope]) -> int:
        return gyroscope.value.z

    @classmethod
    def accelerometer(cls, in_report: InReport) -> Accelerometer:
        return Accelerometer(
            x=cls._sensor_axis(in_report.accel_x_1, in_report.accel_x_0),
            y=cls._sensor_axis(in_report.accel_y_1, in_report.accel_y_0),
            z=cls._sensor_axis(in_report.accel_z_1, in_report.accel_z_0),
        )

    @classmethod
    def accelerometer_x(cls, _: InReport, accelerometer: State[Accelerometer]) -> int:
        return accelerometer.value.x

    @classmethod
    def accelerometer_y(cls, _: InReport, accelerometer: State[Accelerometer]) -> int:
        return accelerometer.value.y

    @classmethod
    def accelerometer_z(cls, _: InReport, accelerometer: State[Accelerometer]) -> int:
        return accelerometer.value.z

    @classmethod
    def orientation(cls, _: InReport, accelerometer: State[Accelerometer]) -> Orientation:
        accel: Accelerometer = accelerometer.value
        return Orientation(
            pitch=(math.atan2(-accel.y, -accel.z) + math.pi),
            roll=(math.atan2(-accel.x, -accel.z) + math.pi)
        )

    @classmethod
    def touch_finger_1_active(cls, in_report: InReport) -> bool:
        return cls._touch_active(in_report.touch_1_0)

    @classmethod
    def touch_finger_1_id(cls, in_report: InReport) -> int:
        return cls._touch_id(in_report.touch_1_0)

    @classmethod
    def touch_finger_1_x(cls, in_report: InReport) -> int:
        return cls._touch_x(in_report.touch_1_2, in_report.touch_1_1)

    @classmethod
    def touch_finger_1_y(cls, in_report: InReport) -> int:
        return cls._touch_y(in_report.touch_1_3, in_report.touch_1_2)

    @classmethod
    def touch_finger_1(
            cls,
            _: InReport,
            touch_finger_1_active: State[bool],
            touch_finger_1_id: State[int],
            touch_finger_1_x: State[int],
            touch_finger_1_y: State[int],
    ) -> TouchFinger:
        return TouchFinger(
            active=touch_finger_1_active.value,
            id=touch_finger_1_id.value,
            x=touch_finger_1_x.value,
            y=touch_finger_1_y.value,
        )

    @classmethod
    def touch_finger_2_active(cls, in_report: InReport) -> bool:
        return cls._touch_active(in_report.touch_2_0)

    @classmethod
    def touch_finger_2_id(cls, in_report: InReport) -> int:
        return cls._touch_id(in_report.touch_2_0)

    @classmethod
    def touch_finger_2_x(cls, in_report: InReport) -> int:
        return cls._touch_x(in_report.touch_2_2, in_report.touch_2_1)

    @classmethod
    def touch_finger_2_y(cls, in_report: InReport) -> int:
        return cls._touch_y(in_report.touch_2_3, in_report.touch_2_2)

    @classmethod
    def touch_finger_2(
            cls,
            _: InReport,
            touch_finger_2_active: State[bool],
            touch_finger_2_id: State[int],
            touch_finger_2_x: State[int],
            touch_finger_2_y: State[int],
    ) -> TouchFinger:
        return TouchFinger(
            active=touch_finger_2_active.value,
            id=touch_finger_2_id.value,
            x=touch_finger_2_x.value,
            y=touch_finger_2_y.value,
        )

    @classmethod
    def l2_feedback_active(cls, in_report: InReport) -> bool:
        return cls._feedback_active(in_report.l2_feedback)

    @classmethod
    def l2_feedback_value(cls, in_report: InReport) -> int:
        return cls._feedback_value(in_report.l2_feedback)

    @classmethod
    def l2_feedback(cls, _: InReport, l2_feedback_active: State[bool], l2_feedback_value: State[int]) -> Feedback:
        return Feedback(
            active=l2_feedback_active.value,
            value=l2_feedback_value.value
        )

    @classmethod
    def r2_feedback_active(cls, in_report: InReport) -> bool:
        return cls._feedback_active(in_report.r2_feedback)

    @classmethod
    def r2_feedback_value(cls, in_report: InReport) -> int:
        return cls._feedback_value(in_report.r2_feedback)

    @classmethod
    def r2_feedback(cls, _: InReport, r2_feedback_active: State[bool], r2_feedback_value: State[int]) -> Feedback:
        return Feedback(
            active=r2_feedback_active.value,
            value=r2_feedback_value.value
        )

    @classmethod
    def battery_level_percentage(cls, in_report: InReport) -> float:
        batt_level_raw: int = in_report.battery_0 & 0x0f
        if batt_level_raw > 8:
            batt_level_raw = 8
        batt_level: float = batt_level_raw / 8
        return batt_level * 100

    @classmethod
    def battery_full(cls, in_report: InReport) -> bool:
        return not not (in_report.battery_0 & 0x20)

    @classmethod
    def battery_charging(cls, in_report: InReport) -> bool:
        return not not (in_report.battery_1 & 0x08)

    @classmethod
    def battery(
            cls,
            _: InReport,
            battery_level_percentage: State[float],
            battery_full: State[bool],
            battery_charging: State[bool]
    ) -> Battery:
        return Battery(
            level_percentage=battery_level_percentage.value,
            full=battery_full.value,
            charging=battery_charging.value,
        )

    # ######### HELPERS #############

    @classmethod
    def _feedback_active(cls, feedback: int) -> bool:
        return bool(feedback & 0x10)

    @classmethod
    def _feedback_value(cls, feedback: int) -> int:
        return feedback & 0xff

    @classmethod
    def _sensor_axis(cls, v1: int, v0: int) -> int:
        res: int = ((v1 << 8) | v0)
        if res > 0x7FFF:
            res -= 0x10000
        return res

    @classmethod
    def _touch_active(cls, t_0: int) -> bool:
        return not (t_0 & 0x80)

    @classmethod
    def _touch_id(cls, t_0: int) -> int:
        return t_0 & 0x7F

    @classmethod
    def _touch_x(cls, t_2: int, t_1: int) -> int:
        return ((t_2 & 0x0F) << 8) | t_1

    @classmethod
    def _touch_y(cls, t_3: int, t_2: int) -> int:
        return (t_3 << 4) | ((t_2 & 0xF0) >> 4)
