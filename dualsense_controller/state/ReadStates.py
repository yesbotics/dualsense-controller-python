import math
import time
from typing import Final

from dualsense_controller import ConnectionType
from dualsense_controller.report import InReport
from dualsense_controller.state import (
    Accelerometer, BaseStates, Gyroscope, JoyStick,
    Orientation, ReadStateName, RestrictedStateAccess, State, StateValueCalc, StateValueMapper
)
from .common import Battery, Feedback, Number, StateChangeCb, StateValueMapping, StateValueType, \
    TouchFinger, compare_accelerometer, \
    compare_battery, compare_feedback, compare_gyroscope, \
    compare_joystick, \
    compare_orientation, \
    compare_shoulder_key, compare_touch_finger


class ReadStates(BaseStates[ReadStateName]):

    def __init__(
            self,
            left_joystick_deadzone: Number = 0,
            right_joystick_deadzone: Number = 0,
            left_shoulder_key_deadzone: Number = 0,
            right_shoulder_key_deadzone: Number = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            state_value_mapping: StateValueMapping = StateValueMapping.DEFAULT,
            enforce_update: bool = True,
            trigger_change_after_all_values_set: bool = True,
    ):
        super().__init__(
            StateValueMapper(
                mapping=state_value_mapping,
                left_joystick_deadzone=left_joystick_deadzone,
                right_joystick_deadzone=right_joystick_deadzone,
                left_shoulder_key_deadzone=left_shoulder_key_deadzone,
                right_shoulder_key_deadzone=right_shoulder_key_deadzone,
            )
        )
        # CONST
        self._trigger_change_after_all_values_set: Final[bool] = trigger_change_after_all_values_set
        self._states_to_trigger_after_all_states_set: Final[list[State]] = []
        # VAR
        self._timestamp: int | None = None
        self._in_report: InReport | None = None

        # INIT STICKS
        self._left_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_x_mapped_to_raw,
        )
        self._left_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_y_mapped_to_raw,
        )
        self._left_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK,
            enforce_update=enforce_update,
            default_value=JoyStick(),
            depends_on=[self._left_stick_x, self._left_stick_y],
            compare_fn=compare_joystick,
            deadzone=self._state_value_mapper.left_stick_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_mapped_to_raw,
        )
        self._right_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_x_mapped_to_raw,
        )
        self._right_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_y_mapped_to_raw,
        )
        self._right_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK,
            enforce_update=enforce_update,
            default_value=JoyStick(),
            depends_on=[self._right_stick_x, self._right_stick_y],
            compare_fn=compare_joystick,
            deadzone=self._state_value_mapper.right_stick_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_mapped_to_raw,
        )

        # INIT GYRO, ACCEL, ORIENT
        self._gyroscope_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_X,
            enforce_update=enforce_update,
        )
        self._gyroscope_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Y,
            enforce_update=enforce_update,
        )
        self._gyroscope_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Z,
            enforce_update=enforce_update,
        )
        self._gyroscope: Final[State[Gyroscope]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE,
            enforce_update=enforce_update,
            default_value=Gyroscope(),
            depends_on=[self._gyroscope_x, self._gyroscope_y, self._gyroscope_z],
            compare_fn=compare_gyroscope,
            threshold=gyroscope_threshold,
        )
        self._accelerometer_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_X,
            enforce_update=enforce_update,
        )
        self._accelerometer_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Y,
            enforce_update=enforce_update,
        )
        self._accelerometer_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Z,
            enforce_update=enforce_update,
        )
        self._accelerometer: Final[State[Accelerometer]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER,
            enforce_update=enforce_update,
            default_value=Accelerometer(),
            depends_on=[self._accelerometer_x, self._accelerometer_y, self._accelerometer_z],
            compare_fn=compare_accelerometer,
            threshold=accelerometer_threshold,
        )
        self._orientation: Final[State[Orientation]] = self._create_and_register_state(
            ReadStateName.ORIENTATION,
            enforce_update=enforce_update,
            default_value=Orientation(0, 0, 0),
            depends_on=[self._gyroscope, self._accelerometer],
            compare_fn=compare_orientation,
            threshold=orientation_threshold,
            raw_to_mapped_fn=lambda raw: Orientation(
                round(math.degrees(raw.pitch), 2),
                round(math.degrees(raw.roll), 2)
            ),
        )

        # INIT SHOULDER KEYS
        self._l2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2,
            enforce_update=enforce_update,
            compare_fn=compare_shoulder_key,
            deadzone=self._state_value_mapper.left_shoulder_key_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.left_shoulder_key_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_shoulder_key_mapped_to_raw,
        )
        self._r2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2,
            enforce_update=enforce_update,
            compare_fn=compare_shoulder_key,
            deadzone=self._state_value_mapper.right_shoulder_key_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.right_shoulder_key_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_shoulder_key_mapped_to_raw,
        )

        # INIT DIG BTN

        self._dpad: Final[State[int]] = self._create_and_register_state(
            ReadStateName.DPAD,
            enforce_update=enforce_update,
        )
        self._btn_up: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_UP,
            enforce_update=enforce_update,
            depends_on=[self._dpad],
        )
        self._btn_left: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_LEFT,
            enforce_update=enforce_update,
            depends_on=[self._dpad],
        )
        self._btn_down: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_DOWN,
            enforce_update=enforce_update,
            depends_on=[self._dpad],
        )
        self._btn_right: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_RIGHT,
            enforce_update=enforce_update,
            depends_on=[self._dpad],
        )

        self._btn_square: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_SQUARE,
            enforce_update=enforce_update,
        )
        self._btn_cross: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CROSS,
            enforce_update=enforce_update,
        )
        self._btn_circle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CIRCLE,
            enforce_update=enforce_update,
        )
        self._btn_triangle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TRIANGLE,
            enforce_update=enforce_update,
        )
        self._btn_l1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L1,
            enforce_update=enforce_update,
        )
        self._btn_r1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R1,
            enforce_update=enforce_update,
        )
        self._btn_l2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L2,
            enforce_update=enforce_update,
        )
        self._btn_r2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R2,
            enforce_update=enforce_update,
        )
        self._btn_create: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CREATE,
            enforce_update=enforce_update,
        )
        self._btn_options: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_OPTIONS,
            enforce_update=enforce_update,
        )
        self._btn_l3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L3,
            enforce_update=enforce_update,
        )
        self._btn_r3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R3,
            enforce_update=enforce_update,
        )
        self._btn_ps: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_PS,
            enforce_update=enforce_update,
        )
        self._btn_touchpad: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TOUCHPAD,
            enforce_update=enforce_update,
        )
        self._btn_mute: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_MUTE,
            enforce_update=enforce_update,
        )

        # INIT TOUCH
        self._touch_finger_1_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_ACTIVE,
            enforce_update=enforce_update,
        )
        self._touch_finger_1_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_ID,
            enforce_update=enforce_update,
        )
        self._touch_finger_1_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_X,
            enforce_update=enforce_update,
        )
        self._touch_finger_1_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_Y,
            enforce_update=enforce_update,
        )
        self._touch_finger_1: Final[State[TouchFinger]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1,
            enforce_update=enforce_update,
            compare_fn=compare_touch_finger,
            depends_on=[
                self._touch_finger_1_active,
                self._touch_finger_1_id,
                self._touch_finger_1_x,
                self._touch_finger_1_y
            ]
        )

        self._touch_finger_2_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_ACTIVE,
            enforce_update=enforce_update,
        )
        self._touch_finger_2_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_ID,
            enforce_update=enforce_update,
        )
        self._touch_finger_2_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_X,
            enforce_update=enforce_update,
        )
        self._touch_finger_2_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_Y,
            enforce_update=enforce_update,
        )
        self._touch_finger_2: Final[State[TouchFinger]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2,
            enforce_update=enforce_update,
            compare_fn=compare_touch_finger,
            depends_on=[
                self._touch_finger_1,
                self._touch_finger_2_active,
                self._touch_finger_2_id,
                self._touch_finger_2_x,
                self._touch_finger_2_y
            ]
        )

        # INIT FEEDBACK
        self._l2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_ACTIVE,
            enforce_update=enforce_update,
        )
        self._l2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_VALUE,
            enforce_update=enforce_update,
        )
        self._l2_feedback: Final[State[Feedback]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK,
            enforce_update=enforce_update,
            depends_on=[self._l2_feedback_active, self._l2_feedback_value],
            compare_fn=compare_feedback
        )

        self._r2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_ACTIVE,
            enforce_update=enforce_update,
        )
        self._r2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_VALUE,
            enforce_update=enforce_update,
        )
        self._r2_feedback: Final[State[Feedback]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK,
            enforce_update=enforce_update,
            depends_on=[self._r2_feedback_active, self._r2_feedback_value],
            compare_fn=compare_feedback
        )

        # INIT BATT
        self._battery_level_percentage: Final[State[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT,
            enforce_update=enforce_update,
            ignore_none=False,
        )
        self._battery_full: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL,
            enforce_update=enforce_update,
            ignore_none=False,
        )
        self._battery_charging: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING,
            enforce_update=enforce_update,
            ignore_none=False,
        )
        self._battery: Final[State[Battery]] = self._create_and_register_state(
            ReadStateName.BATTERY,
            enforce_update=enforce_update,
            ignore_none=False,
            depends_on=[self._battery_level_percentage, self._battery_full, self._battery_charging],
            compare_fn=compare_battery
        )

    # #################### PRIVATE #######################

    def _handle_state(
            self,
            state: State[StateValueType],
            value: StateValueType,
    ) -> StateValueType | None:
        if (
                state.enforce_update
                or state.has_listeners
                or state.has_listened_dependents
                or state.has_changed_dependencies
        ):
            if self._trigger_change_after_all_values_set:
                state.set_value_without_triggering_change(value, self._timestamp)
                self._states_to_trigger_after_all_states_set.append(state)
            else:
                state.set_value(value, timestamp=self._timestamp)
            return value
        return None

    # #################### PUBLIC #######################

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        now_timestamp: int = time.perf_counter_ns()
        diff_timestamp: int = now_timestamp - self._timestamp if self._timestamp is not None else 0
        # print('diff_timestamp ns', diff_timestamp)

        self._timestamp = now_timestamp
        self._in_report = in_report

        # #### ANALOG STICKS #####

        self._handle_state(self._left_stick, JoyStick(x=in_report.axes_0, y=in_report.axes_1))
        # use values from stick because deadzone calc is done there
        self._handle_state(self._left_stick_x, self._left_stick.value.x)
        self._handle_state(self._left_stick_y, self._left_stick.value.y)

        self._handle_state(self._right_stick, JoyStick(x=in_report.axes_2, y=in_report.axes_3))
        # use values from stick because deadzone calc is done there
        self._handle_state(self._right_stick_x, self._right_stick.value.x)
        self._handle_state(self._right_stick_y, self._right_stick.value.y)

        # ##### SHOULDER KEYS #####
        self._handle_state(self._l2, in_report.axes_4)
        self._handle_state(self._r2, in_report.axes_5)

        # ##### BUTTONS #####
        self._handle_state(self._dpad, in_report.buttons_0 & 0x0f)
        self._handle_state(self._btn_up, self._dpad.value == 0 or self._dpad.value == 1 or self._dpad.value == 7)
        self._handle_state(self._btn_down, self._dpad.value == 3 or self._dpad.value == 4 or self._dpad.value == 5)
        self._handle_state(self._btn_left, self._dpad.value == 5 or self._dpad.value == 6 or self._dpad.value == 7)
        self._handle_state(self._btn_right, self._dpad.value == 1 or self._dpad.value == 2 or self._dpad.value == 3)

        self._handle_state(self._btn_cross, bool(in_report.buttons_0 & 0x20))
        self._handle_state(self._btn_r1, bool(in_report.buttons_1 & 0x02))
        self._handle_state(self._btn_square, bool(in_report.buttons_0 & 0x10))
        self._handle_state(self._btn_circle, bool(in_report.buttons_0 & 0x40))
        self._handle_state(self._btn_triangle, bool(in_report.buttons_0 & 0x80))
        self._handle_state(self._btn_l1, bool(in_report.buttons_1 & 0x01))
        self._handle_state(self._btn_l2, bool(in_report.buttons_1 & 0x04))
        self._handle_state(self._btn_r2, bool(in_report.buttons_1 & 0x08))
        self._handle_state(self._btn_create, bool(in_report.buttons_1 & 0x10))
        self._handle_state(self._btn_options, bool(in_report.buttons_1 & 0x20))
        self._handle_state(self._btn_l3, bool(in_report.buttons_1 & 0x40))
        self._handle_state(self._btn_r3, bool(in_report.buttons_1 & 0x80))
        self._handle_state(self._btn_ps, bool(in_report.buttons_2 & 0x01))
        self._handle_state(self._btn_mute, bool(in_report.buttons_2 & 0x04))
        self._handle_state(self._btn_touchpad, bool(in_report.buttons_2 & 0x02))

        # following not supported for BT01
        if connection_type == ConnectionType.BT_01:
            return

        # ##### GYRO #####

        self._handle_state(self._gyroscope, Gyroscope(
            x=StateValueCalc.sensor_axis(in_report.gyro_x_1, in_report.gyro_x_0),
            y=StateValueCalc.sensor_axis(in_report.gyro_y_1, in_report.gyro_y_0),
            z=StateValueCalc.sensor_axis(in_report.gyro_z_1, in_report.gyro_z_0),
        ))
        self._handle_state(self._gyroscope_x, self._gyroscope.value.x)
        self._handle_state(self._gyroscope_y, self._gyroscope.value.y)
        self._handle_state(self._gyroscope_z, self._gyroscope.value.z)

        # ##### ACCEL #####
        self._handle_state(self._accelerometer, Accelerometer(
            x=StateValueCalc.sensor_axis(in_report.accel_x_1, in_report.accel_x_0),
            y=StateValueCalc.sensor_axis(in_report.accel_y_1, in_report.accel_y_0),
            z=StateValueCalc.sensor_axis(in_report.accel_z_1, in_report.accel_z_0),
        ))
        self._handle_state(self._accelerometer_x, self._accelerometer.value.x)
        self._handle_state(self._accelerometer_y, self._accelerometer.value.y)
        self._handle_state(self._accelerometer_z, self._accelerometer.value.z)

        # ##### ORIENTATION #####
        # self._handle_state(self._orientation, StateValueCalc.orientation_complementary_filter(
        #     gyro=self._gyroscope.value,
        #     accel=self.accelerometer.value,
        #     previous_orientation=self._orientation.value,
        # ))
        self._handle_state(self._orientation, StateValueCalc.orientation_simple(
            accel=self.accelerometer.value,
        ))

        # ##### TOUCH 0 #####
        self._handle_state(self._touch_finger_1_active, StateValueCalc.touch_active(in_report.touch_1_0))
        self._handle_state(self._touch_finger_1_id, StateValueCalc.touch_id(in_report.touch_1_0))
        self._handle_state(self._touch_finger_1_x, StateValueCalc.touch_x(in_report.touch_1_2, in_report.touch_1_1))
        self._handle_state(self._touch_finger_1_y, StateValueCalc.touch_y(in_report.touch_1_3, in_report.touch_1_2))
        self._handle_state(self._touch_finger_1, TouchFinger(
            active=self._touch_finger_1_active.value,
            id=self._touch_finger_1_id.value,
            x=self._touch_finger_1_x.value,
            y=self._touch_finger_1_y.value,
        ))

        # ##### TOUCH 1 #####
        self._handle_state(self._touch_finger_2_active, StateValueCalc.touch_active(in_report.touch_2_0))
        self._handle_state(self._touch_finger_2_id, StateValueCalc.touch_id(in_report.touch_2_0))
        self._handle_state(self._touch_finger_2_x, StateValueCalc.touch_x(in_report.touch_2_2, in_report.touch_2_1))
        self._handle_state(self._touch_finger_2_y, StateValueCalc.touch_y(in_report.touch_2_3, in_report.touch_2_2))
        self._handle_state(self._touch_finger_2, TouchFinger(
            active=self._touch_finger_2_active.value,
            id=self._touch_finger_2_id.value,
            x=self._touch_finger_2_x.value,
            y=self._touch_finger_2_y.value,
        ))

        # ##### TRIGGER FEEDBACK #####
        self._handle_state(self._l2_feedback_active, bool(in_report.l2_feedback & 0x10))
        self._handle_state(self._l2_feedback_value, in_report.l2_feedback & 0xff)
        self._handle_state(self._l2_feedback, Feedback(
            active=self._l2_feedback_active.value,
            value=self._l2_feedback_value.value
        ))

        self._handle_state(self._r2_feedback_active, bool(in_report.r2_feedback & 0x10))
        self._handle_state(self._r2_feedback_value, in_report.r2_feedback & 0xff)
        self._handle_state(self._r2_feedback, Feedback(
            active=self._r2_feedback_active.value,
            value=self._r2_feedback_value.value
        ))

        # ##### BATTERY #####
        self._handle_state(self._battery_level_percentage, StateValueCalc.batt_level_percentage(in_report.battery_0))
        self._handle_state(self._battery_full, not not (in_report.battery_0 & 0x20))
        self._handle_state(self._battery_charging, not not (in_report.battery_1 & 0x08))
        self._handle_state(self._battery, Battery(
            level_percentage=self._battery_level_percentage.value,
            full=self._battery_full.value,
            charging=self._battery_charging.value,
        ))

        for state in self._states_to_trigger_after_all_states_set:
            state.trigger_change_if_changed()
        self._states_to_trigger_after_all_states_set.clear()

    def on_change(
            self, name_or_callback: ReadStateName | StateChangeCb, callback: StateChangeCb | None = None
    ):
        if callback is None:
            self.on_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).on_change(callback)

    def on_any_change(self, callback: StateChangeCb):
        for state_name, state in self._states_dict.items():
            state.on_change(callback)

    def remove_change_listener(
            self, name_or_callback: ReadStateName | StateChangeCb, callback: StateChangeCb | None = None
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

    def remove_any_change_listener(self, callback: StateChangeCb) -> None:
        for state_name, state in self._states_dict.items():
            state.remove_change_listener(callback)

    # #################### GETTERS #######################

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
        return self._touch_finger_1_active.restricted_access

    @property
    def touch_0_id(self) -> RestrictedStateAccess[int]:
        return self._touch_finger_1_id.restricted_access

    @property
    def touch_0_x(self) -> RestrictedStateAccess[int]:
        return self._touch_finger_1_x.restricted_access

    @property
    def touch_0_y(self) -> RestrictedStateAccess[int]:
        return self._touch_finger_1_y.restricted_access

    @property
    def touch_1_active(self) -> RestrictedStateAccess[bool]:
        return self._touch_finger_1_active.restricted_access

    @property
    def touch_1_id(self) -> RestrictedStateAccess[int]:
        return self._touch_finger_2_id.restricted_access

    @property
    def touch_1_x(self) -> RestrictedStateAccess[int]:
        return self._touch_finger_2_x.restricted_access

    @property
    def touch_1_y(self) -> RestrictedStateAccess[int]:
        return self._touch_finger_2_y.restricted_access

    @property
    def l2_feedback_active(self) -> RestrictedStateAccess[bool]:
        return self._l2_feedback_active.restricted_access

    @property
    def l2_feedback_value(self) -> RestrictedStateAccess[int]:
        return self._l2_feedback_value.restricted_access

    @property
    def l2_feedback(self) -> RestrictedStateAccess[Feedback]:
        return self._l2_feedback.restricted_access

    @property
    def r2_feedback_active(self) -> RestrictedStateAccess[bool]:
        return self._r2_feedback_active.restricted_access

    @property
    def r2_feedback_value(self) -> RestrictedStateAccess[int]:
        return self._r2_feedback_value.restricted_access

    @property
    def r2_feedback(self) -> RestrictedStateAccess[Feedback]:
        return self._r2_feedback.restricted_access

    @property
    def battery_level_percentage(self) -> RestrictedStateAccess[float]:
        return self._battery_level_percentage.restricted_access

    @property
    def battery_full(self) -> RestrictedStateAccess[bool]:
        return self._battery_full.restricted_access

    @property
    def battery_charging(self) -> RestrictedStateAccess[int]:
        return self._battery_charging.restricted_access

    @property
    def battery(self) -> RestrictedStateAccess[Battery]:
        return self._battery.restricted_access

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

    @property
    def touch_finger_1(self) -> RestrictedStateAccess[TouchFinger]:
        return self._touch_finger_1.restricted_access

    @property
    def touch_finger_2(self) -> RestrictedStateAccess[TouchFinger]:
        return self._touch_finger_2.restricted_access
