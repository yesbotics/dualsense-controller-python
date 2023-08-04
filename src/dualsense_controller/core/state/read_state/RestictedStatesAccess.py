from __future__ import annotations

from typing import Final

from dualsense_controller.core.state.read_state.ReadStates import ReadStates
from dualsense_controller.core.state.read_state.RestrictedStateAccess import RestrictedStateAccess
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Feedback, Gyroscope, JoyStick, \
    Orientation, TouchFinger


class RestrictedStatesAccess:

    def __init__(self, read_states: ReadStates):
        self.left_stick_x: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.left_stick_x)
        self.left_stick_y: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.left_stick_y)
        self.right_stick_x: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.right_stick_x)
        self.right_stick_y: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.right_stick_y)
        self.l2: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.l2)
        self.r2: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.r2)
        self.btn_up: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_up)
        self.btn_left: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_left)
        self.btn_down: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_down)
        self.btn_right: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_right)
        self.btn_square: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_square)
        self.btn_cross: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_cross)
        self.btn_circle: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_circle)
        self.btn_triangle: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_triangle)
        self.btn_l1: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_l1)
        self.btn_r1: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_r1)
        self.btn_l2: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_l2)
        self.btn_r2: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_r2)
        self.btn_create: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_create)
        self.btn_options: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_options)
        self.btn_l3: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_l3)
        self.btn_r3: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_r3)
        self.btn_ps: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_ps)
        self.btn_touchpad: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_touchpad)
        self.btn_mute: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.btn_mute)
        self.gyroscope_x: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.gyroscope_x)
        self.gyroscope_y: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.gyroscope_y)
        self.gyroscope_z: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.gyroscope_z)
        self.accelerometer_x: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.accelerometer_x)
        self.accelerometer_y: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.accelerometer_y)
        self.accelerometer_z: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.accelerometer_z)
        self.touch_finger_1_active: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(
            read_states.touch_finger_1_active)
        self.touch_finger_1_id: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.touch_finger_1_id)
        self.touch_finger_1_x: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.touch_finger_1_x)
        self.touch_finger_1_y: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.touch_finger_1_y)
        self.touch_finger_2_active: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(
            read_states.touch_finger_2_active)
        self.touch_finger_2_id: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.touch_finger_2_id)
        self.touch_finger_2_x: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.touch_finger_2_x)
        self.touch_finger_2_y: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.touch_finger_2_y)
        self.l2_feedback_active: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(
            read_states.l2_feedback_active)
        self.l2_feedback_value: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.l2_feedback_value)
        self.l2_feedback: Final[RestrictedStateAccess[Feedback]] = RestrictedStateAccess(read_states.l2_feedback)
        self.r2_feedback_active: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(
            read_states.r2_feedback_active)
        self.r2_feedback_value: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.r2_feedback_value)
        self.r2_feedback: Final[RestrictedStateAccess[Feedback]] = RestrictedStateAccess(read_states.r2_feedback)
        self.battery_level_percentage: Final[RestrictedStateAccess[float]] = RestrictedStateAccess(
            read_states.battery_level_percentage)
        self.battery_full: Final[RestrictedStateAccess[bool]] = RestrictedStateAccess(read_states.battery_full)
        self.battery_charging: Final[RestrictedStateAccess[int]] = RestrictedStateAccess(read_states.battery_charging)
        self.battery: Final[RestrictedStateAccess[Battery]] = RestrictedStateAccess(read_states.battery)
        self.left_stick: Final[RestrictedStateAccess[JoyStick]] = RestrictedStateAccess(read_states.left_stick)
        self.right_stick: Final[RestrictedStateAccess[JoyStick]] = RestrictedStateAccess(read_states.right_stick)
        self.gyroscope: Final[RestrictedStateAccess[Gyroscope]] = RestrictedStateAccess(read_states.gyroscope)
        self.accelerometer: Final[RestrictedStateAccess[Accelerometer]] = RestrictedStateAccess(
            read_states.accelerometer)
        self.orientation: Final[RestrictedStateAccess[Orientation]] = RestrictedStateAccess(read_states.orientation)
        self.touch_finger_1: Final[RestrictedStateAccess[TouchFinger]] = RestrictedStateAccess(
            read_states.touch_finger_1)
        self.touch_finger_2: Final[RestrictedStateAccess[TouchFinger]] = RestrictedStateAccess(
            read_states.touch_finger_2)
