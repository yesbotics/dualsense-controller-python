import math

from dualsense_controller.core.report.in_report import InReport
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, TriggerFeedback, Gyroscope, \
    JoyStick, \
    Orientation, \
    TouchFinger


class ValueCalc:

    # ########################################## SET ONLY NEEDED FOR TESTING ##########################################
    @classmethod
    def set_left_stick(cls, in_report: InReport, value: JoyStick) -> None:
        cls.set_left_stick_x(in_report, value.x)
        cls.set_left_stick_y(in_report, value.y)

    @classmethod
    def set_left_stick_x(cls, in_report: InReport, value: int) -> None:
        in_report.axes_0 = value

    @classmethod
    def set_left_stick_y(cls, in_report: InReport, value: int) -> None:
        in_report.axes_1 = value

    @classmethod
    def set_right_stick(cls, in_report: InReport, value: JoyStick) -> None:
        cls.set_right_stick_x(in_report, value.x)
        cls.set_right_stick_y(in_report, value.y)

    @classmethod
    def set_right_stick_x(cls, in_report: InReport, value: int) -> None:
        in_report.axes_2 = value

    @classmethod
    def set_right_stick_y(cls, in_report: InReport, value: int) -> None:
        in_report.axes_3 = value

    @classmethod
    def set_left_trigger(cls, in_report: InReport, value: int) -> None:
        in_report.axes_4 = value

    @classmethod
    def set_right_trigger(cls, in_report: InReport, value: int) -> None:
        in_report.axes_5 = value

    @classmethod
    def set_btn_cross(cls, in_report: InReport, value: bool) -> None:
        in_report.buttons_0 = in_report.buttons_0 | 0x10 if value else in_report.buttons_0 & 0xEF

    @classmethod
    def set_btn_square(cls, in_report: InReport, value: bool) -> None:
        in_report.buttons_0 = in_report.buttons_0 | 0x20 if value else in_report.buttons_0 & 0xDF

    # ########################################## GET ###############################################
    @classmethod
    def get_left_stick(cls, in_report: InReport) -> JoyStick:
        return JoyStick(x=in_report.axes_0, y=in_report.axes_1)

    @classmethod
    def get_left_stick_x(cls, _: InReport, left_stick: State[JoyStick]) -> int:
        return left_stick.value_raw.x

    @classmethod
    def get_left_stick_y(cls, _: InReport, left_stick: State[JoyStick]) -> int:
        return left_stick.value_raw.y

    @classmethod
    def get_right_stick(cls, in_report: InReport) -> JoyStick:
        return JoyStick(x=in_report.axes_2, y=in_report.axes_3)

    @classmethod
    def get_right_stick_x(cls, _: InReport, right_stick: State[JoyStick]) -> int:
        return right_stick.value_raw.x

    @classmethod
    def get_right_stick_y(cls, _: InReport, right_stick: State[JoyStick]) -> int:
        return right_stick.value_raw.y

    @classmethod
    def get_left_trigger_value(cls, in_report: InReport) -> int:
        return in_report.axes_4

    @classmethod
    def get_right_trigger_value(cls, in_report: InReport) -> int:
        return in_report.axes_5

    @classmethod
    def get_dpad(cls, in_report: InReport) -> int:
        return in_report.buttons_0 & 0x0f

    @classmethod
    def get_btn_up(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value_raw == 0 or dpad.value_raw == 1 or dpad.value_raw == 7

    @classmethod
    def get_btn_down(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value_raw == 3 or dpad.value_raw == 4 or dpad.value_raw == 5

    @classmethod
    def get_btn_left(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value_raw == 5 or dpad.value_raw == 6 or dpad.value_raw == 7

    @classmethod
    def get_btn_right(cls, _: InReport, dpad: State[int]) -> bool:
        return dpad.value_raw == 1 or dpad.value_raw == 2 or dpad.value_raw == 3

    @classmethod
    def get_btn_cross(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x20)

    @classmethod
    def get_btn_r1(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x02)

    @classmethod
    def get_btn_square(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x10)

    @classmethod
    def get_btn_circle(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x40)

    @classmethod
    def get_btn_triangle(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_0 & 0x80)

    @classmethod
    def get_btn_l1(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x01)

    @classmethod
    def get_btn_l2(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x04)

    @classmethod
    def get_btn_r2(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x08)

    @classmethod
    def get_btn_create(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x10)

    @classmethod
    def btn_options(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x20)

    @classmethod
    def get_btn_l3(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x40)

    @classmethod
    def get_btn_r3(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_1 & 0x80)

    @classmethod
    def get_btn_ps(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_2 & 0x01)

    @classmethod
    def get_btn_mute(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_2 & 0x04)

    @classmethod
    def get_btn_touchpad(cls, in_report: InReport) -> bool:
        return bool(in_report.buttons_2 & 0x02)

    @classmethod
    def get_gyroscope(cls, in_report: InReport) -> Gyroscope:
        return Gyroscope(
            x=cls._get_sensor_axis(in_report.gyro_x_1, in_report.gyro_x_0),
            y=cls._get_sensor_axis(in_report.gyro_y_1, in_report.gyro_y_0),
            z=cls._get_sensor_axis(in_report.gyro_z_1, in_report.gyro_z_0),
        )

    @classmethod
    def get_gyroscope_x(cls, _: InReport, gyroscope: State[Gyroscope]) -> int:
        return gyroscope.value_raw.x

    @classmethod
    def get_gyroscope_y(cls, _: InReport, gyroscope: State[Gyroscope]) -> int:
        return gyroscope.value_raw.y

    @classmethod
    def get_gyroscope_z(cls, _: InReport, gyroscope: State[Gyroscope]) -> int:
        return gyroscope.value_raw.z

    @classmethod
    def get_accelerometer(cls, in_report: InReport) -> Accelerometer:
        return Accelerometer(
            x=cls._get_sensor_axis(in_report.accel_x_1, in_report.accel_x_0),
            y=cls._get_sensor_axis(in_report.accel_y_1, in_report.accel_y_0),
            z=cls._get_sensor_axis(in_report.accel_z_1, in_report.accel_z_0),
        )

    @classmethod
    def get_accelerometer_x(cls, _: InReport, accelerometer: State[Accelerometer]) -> int:
        return accelerometer.value_raw.x

    @classmethod
    def get_accelerometer_y(cls, _: InReport, accelerometer: State[Accelerometer]) -> int:
        return accelerometer.value_raw.y

    @classmethod
    def get_accelerometer_z(cls, _: InReport, accelerometer: State[Accelerometer]) -> int:
        return accelerometer.value_raw.z

    @classmethod
    def get_orientation(cls, _: InReport, accelerometer: State[Accelerometer]) -> Orientation:
        accel: Accelerometer = accelerometer.value_raw
        return Orientation(
            pitch=(math.atan2(-accel.y, -accel.z) + math.pi),
            roll=(math.atan2(-accel.x, -accel.z) + math.pi)
        )

    @classmethod
    def get_touch_finger_1_active(cls, in_report: InReport) -> bool:
        return cls._get_touch_active(in_report.touch_1_0)

    @classmethod
    def get_touch_finger_1_id(cls, in_report: InReport) -> int:
        return cls._get_touch_id(in_report.touch_1_0)

    @classmethod
    def get_touch_finger_1_x(cls, in_report: InReport) -> int:
        return cls._get_touch_x(in_report.touch_1_2, in_report.touch_1_1)

    @classmethod
    def get_touch_finger_1_y(cls, in_report: InReport) -> int:
        return cls._get_touch_y(in_report.touch_1_3, in_report.touch_1_2)

    @classmethod
    def get_touch_finger_1(
            cls,
            _: InReport,
            touch_finger_1_active: State[bool],
            touch_finger_1_id: State[int],
            touch_finger_1_x: State[int],
            touch_finger_1_y: State[int],
    ) -> TouchFinger:
        return TouchFinger(
            active=touch_finger_1_active.value_raw,
            id=touch_finger_1_id.value_raw,
            x=touch_finger_1_x.value_raw,
            y=touch_finger_1_y.value_raw,
        )

    @classmethod
    def get_touch_finger_2_active(cls, in_report: InReport) -> bool:
        return cls._get_touch_active(in_report.touch_2_0)

    @classmethod
    def get_touch_finger_2_id(cls, in_report: InReport) -> int:
        return cls._get_touch_id(in_report.touch_2_0)

    @classmethod
    def get_touch_finger_2_x(cls, in_report: InReport) -> int:
        return cls._get_touch_x(in_report.touch_2_2, in_report.touch_2_1)

    @classmethod
    def get_touch_finger_2_y(cls, in_report: InReport) -> int:
        return cls._get_touch_y(in_report.touch_2_3, in_report.touch_2_2)

    @classmethod
    def get_touch_finger_2(
            cls,
            _: InReport,
            touch_finger_2_active: State[bool],
            touch_finger_2_id: State[int],
            touch_finger_2_x: State[int],
            touch_finger_2_y: State[int],
    ) -> TouchFinger:
        return TouchFinger(
            active=touch_finger_2_active.value_raw,
            id=touch_finger_2_id.value_raw,
            x=touch_finger_2_x.value_raw,
            y=touch_finger_2_y.value_raw,
        )

    @classmethod
    def get_left_trigger_feedback_active(cls, in_report: InReport) -> bool:
        return cls._get_trigger_feedback_active(in_report.left_trigger_feedback)

    @classmethod
    def get_left_trigger_feedback_value(cls, in_report: InReport) -> int:
        return cls._get_trigger_feedback_value(in_report.left_trigger_feedback)

    @classmethod
    def get_left_trigger_feedback(cls, _: InReport, l2_feedback_active: State[bool],
                                  l2_feedback_value: State[int]) -> TriggerFeedback:
        return TriggerFeedback(
            active=l2_feedback_active.value_raw,
            value=l2_feedback_value.value_raw
        )

    @classmethod
    def get_right_trigger_feedback_active(cls, in_report: InReport) -> bool:
        return cls._get_trigger_feedback_active(in_report.right_trigger_feedback)

    @classmethod
    def get_right_trigger_feedback_value(cls, in_report: InReport) -> int:
        return cls._get_trigger_feedback_value(in_report.right_trigger_feedback)

    @classmethod
    def get_right_trigger_feedback(cls, _: InReport, r2_feedback_active: State[bool],
                                   r2_feedback_value: State[int]) -> TriggerFeedback:
        return TriggerFeedback(
            active=r2_feedback_active.value_raw,
            value=r2_feedback_value.value_raw
        )

    @classmethod
    def get_battery_level_percentage(cls, in_report: InReport) -> float:
        batt_level_raw: int = in_report.battery_0 & 0x0f
        if batt_level_raw > 8:
            batt_level_raw = 8
        batt_level: float = batt_level_raw / 8
        return batt_level * 100

    @classmethod
    def get_battery_full(cls, in_report: InReport) -> bool:
        return not not (in_report.battery_0 & 0x20)

    @classmethod
    def battery_charging(cls, in_report: InReport) -> bool:
        return not not (in_report.battery_1 & 0x08)

    @classmethod
    def get_battery(
            cls,
            _: InReport,
            battery_level_percentage: State[float],
            battery_full: State[bool],
            battery_charging: State[bool]
    ) -> Battery:
        return Battery(
            level_percentage=battery_level_percentage.value_raw,
            full=battery_full.value_raw,
            charging=battery_charging.value_raw,
        )

    # ######### HELPERS #############

    @classmethod
    def _get_trigger_feedback_active(cls, feedback: int) -> bool:
        return bool(feedback & 0x10)

    @classmethod
    def _get_trigger_feedback_value(cls, feedback: int) -> int:
        return feedback & 0xff

    @classmethod
    def _get_sensor_axis(cls, v1: int, v0: int) -> int:
        res: int = ((v1 << 8) | v0)
        if res > 0x7FFF:
            res -= 0x10000
        return res

    @classmethod
    def _get_touch_active(cls, t_0: int) -> bool:
        return not (t_0 & 0x80)

    @classmethod
    def _get_touch_id(cls, t_0: int) -> int:
        return t_0 & 0x7F

    @classmethod
    def _get_touch_x(cls, t_2: int, t_1: int) -> int:
        return ((t_2 & 0x0F) << 8) | t_1

    @classmethod
    def _get_touch_y(cls, t_3: int, t_2: int) -> int:
        return (t_3 << 4) | ((t_2 & 0xF0) >> 4)
