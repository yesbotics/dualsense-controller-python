from typing import Callable, Final

from dualsense_controller import ConnectionType
from dualsense_controller.report import InReport
from dualsense_controller.state import (
    Accelerometer, AnyStateChangeCallback, BaseStates, Gyroscope, JoyStick,
    Orientation, ReadStateName, RestrictedStateAccess, State, StateChangeCallback,
    calc_orientation, calc_sensor_axis, calc_touch_id, calc_touch_x, calc_touch_y
)
from .common import StateValueMapping, StateValueType, compare_accel, compare_gyroscope, compare_joystick, \
    compare_orientation, \
    compare_shoulder_key


class ReadStates(BaseStates[ReadStateName]):

    def __init__(
            self,
            joystick_deadzone: int = 0,
            shoulder_key_deadzone: int = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            state_value_mapping: StateValueMapping = StateValueMapping.FOR_NOOBS,
            enforce_update: bool = True,
            trigger_change_lazy: bool = True,
    ):
        super().__init__()

        self._trigger_change_after_all_values_set: Final[bool] = trigger_change_lazy
        self._states_to_trigger_after_all_states_set: Final[list[State]] = []
        self._state_value_mapping: Final[StateValueMapping] = state_value_mapping

        # INIT STICKS
        self._left_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X,
            enforce_update=enforce_update,
        )
        self._left_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y,
            enforce_update=enforce_update,
        )
        self._left_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK,
            is_based_on=[self._left_stick_x, self._left_stick_y],
            compare_fn=compare_joystick,
            deadzone=joystick_deadzone,
            ignore_initial_none=False,
            enforce_update=enforce_update,
        )
        self._right_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X,
            enforce_update=enforce_update,
        )
        self._right_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y,
            enforce_update=enforce_update,
        )
        self._right_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK,
            is_based_on=[self._right_stick_x, self._right_stick_y],
            compare_fn=compare_joystick,
            deadzone=joystick_deadzone,
            ignore_initial_none=False,
            enforce_update=enforce_update,
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
            is_based_on=[self._gyroscope_x, self._gyroscope_y, self._gyroscope_z],
            compare_fn=compare_gyroscope,
            threshold=gyroscope_threshold,
            enforce_update=enforce_update,
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
            is_based_on=[self._accelerometer_x, self._accelerometer_y, self._accelerometer_z],
            compare_fn=compare_accel,
            threshold=accelerometer_threshold,
            enforce_update=enforce_update,
        )
        self._orientation: Final[State[Orientation]] = self._create_and_register_state(
            ReadStateName.ORIENTATION,
            is_based_on=[self._gyroscope, self._accelerometer],
            compare_fn=compare_orientation,
            threshold=orientation_threshold,
            enforce_update=enforce_update,
        )

        # INIT SHOULDER KEYS
        self._l2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2,
            compare_fn=compare_shoulder_key,
            deadzone=shoulder_key_deadzone,
            enforce_update=enforce_update,
        )
        self._r2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2,
            compare_fn=compare_shoulder_key,
            deadzone=shoulder_key_deadzone,
            enforce_update=enforce_update,
        )

        # INIT DIG BTN
        self._btn_up: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_UP,
            enforce_update=enforce_update,
        )
        self._btn_left: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_LEFT,
            enforce_update=enforce_update,
        )
        self._btn_down: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_DOWN,
            enforce_update=enforce_update,
        )
        self._btn_right: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_RIGHT,
            enforce_update=enforce_update,
        )
        self._btn_square: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_SQUARE,
            enforce_update=enforce_update,
        )
        self._btn_cross: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CROSS,
            enforce_update=enforce_update,
            ignore_initial_none=False,
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
            ignore_initial_none=False,
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
        self._touch_0_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ACTIVE,
            enforce_update=enforce_update,
        )
        self._touch_0_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ID,
            enforce_update=enforce_update,
        )
        self._touch_0_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_X,
            enforce_update=enforce_update,
        )
        self._touch_0_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_Y,
            enforce_update=enforce_update,
        )
        self._touch_1_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ACTIVE,
            enforce_update=enforce_update,
        )
        self._touch_1_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ID,
            enforce_update=enforce_update,
        )
        self._touch_1_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_X,
            enforce_update=enforce_update,
        )
        self._touch_1_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_Y,
            enforce_update=enforce_update,
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
        self._r2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_ACTIVE,
            enforce_update=enforce_update,
        )
        self._r2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_VALUE,
            enforce_update=enforce_update,
        )

        # INIT BATT
        self._battery_level_percent: Final[State[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT,
            ignore_initial_none=False,
            enforce_update=enforce_update,
        )
        self._battery_full: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL,
            ignore_initial_none=False,
            enforce_update=enforce_update,
        )
        self._battery_charging: Final[State[int]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING,
            ignore_initial_none=False,
            enforce_update=enforce_update,
        )

    # #################### PRIVATE #######################

    def _handle_state(
            self,
            state: State[StateValueType],
            value_or_calc_fn: StateValueType | Callable[[...], StateValueType],
            *args,
            determine_value: bool = False
    ) -> StateValueType | None:
        if determine_value:
            return
        if state.needs_update:
            value_: StateValueType = value_or_calc_fn(*args) if callable(value_or_calc_fn) else value_or_calc_fn
            state.value = value_
            # if self._trigger_change_after_all_values_set:
            #     state.set_value_without_triggering_change(value)
            #     self._states_to_trigger_after_all_states_set.append(self._btn_cross)
            # else:
            #     state.value = value
            return value_
        return

    # #################### PUBLIC #######################

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        # ##### ANALOG STICKS #####
        self._handle_state(self._left_stick_x, in_report.axes_0)
        self._handle_state(self._left_stick_y, in_report.axes_1)
        self._handle_state(self._left_stick, JoyStick(x=self._left_stick_x.value, y=self._left_stick_y.value))
        self._handle_state(self._right_stick_x, in_report.axes_2)
        self._handle_state(self._right_stick_y, in_report.axes_3)
        self._handle_state(self._right_stick, JoyStick(x=self._right_stick_x.value, y=self._right_stick_y.value))

        # ##### SHOULDER KEYS #####
        self._handle_state(self._l2, in_report.axes_4)
        self._handle_state(self._r2, in_report.axes_5)

        # ##### BUTTONS #####
        dpad: int = in_report.buttons_0 & 0x0f
        self._handle_state(self._btn_cross, bool(in_report.buttons_0 & 0x20))
        self._handle_state(self._btn_r1, bool(in_report.buttons_1 & 0x02))
        self._handle_state(self._btn_up, dpad == 0 or dpad == 1 or dpad == 7)
        self._handle_state(self._btn_down, dpad == 3 or dpad == 4 or dpad == 5)
        self._handle_state(self._btn_left, dpad == 5 or dpad == 6 or dpad == 7)
        self._handle_state(self._btn_right, dpad == 1 or dpad == 2 or dpad == 3)
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

        self._handle_state(self._gyroscope_x, calc_sensor_axis, in_report.gyro_x_1, in_report.gyro_x_0)
        self._handle_state(self._gyroscope_y, calc_sensor_axis, in_report.gyro_x_1, in_report.gyro_x_0)
        self._handle_state(self._gyroscope_z, calc_sensor_axis, in_report.gyro_x_1, in_report.gyro_x_0)
        self._handle_state(self._gyroscope, Gyroscope(
            x=self._gyroscope_x.value,
            y=self._gyroscope_y.value,
            z=self._gyroscope_z.value,
        ))

        # ##### ACCEL #####
        self._handle_state(self._accelerometer_x, calc_sensor_axis, in_report.gyro_x_1, in_report.gyro_x_0)
        self._handle_state(self._accelerometer_y, calc_sensor_axis, in_report.gyro_x_1, in_report.gyro_x_0)
        self._handle_state(self._accelerometer_z, calc_sensor_axis, in_report.gyro_x_1, in_report.gyro_x_0)
        self._handle_state(self._accelerometer, Accelerometer(
            x=self._accelerometer_x.value,
            y=self._accelerometer_y.value,
            z=self._accelerometer_z.value,
        ))

        # ##### ORIENTATION #####
        self._handle_state(self._orientation, calc_orientation, self._gyroscope, self._accelerometer)

        # ##### TOUCH #####
        touch_0_active: bool = self._handle_state(self._touch_0_active, not (in_report.touch_0_0 & 0x80))
        self._handle_state(
            self._touch_0_id,
            calc_touch_id,
            in_report.touch_0_0,
            determine_value=touch_0_active,
        )
        self._handle_state(
            self._touch_0_x,
            calc_touch_x,
            in_report.touch_0_2,
            in_report.touch_0_1,
            determine_value=touch_0_active
        )
        self._handle_state(
            self._touch_0_y,
            calc_touch_y,
            in_report.touch_0_3,
            in_report.touch_0_2,
            determine_value=touch_0_active
        )

        touch_1_active: bool = self._handle_state(self._touch_1_active, not (in_report.touch_1_0 & 0x80), )
        self._handle_state(
            self._touch_1_id,
            calc_touch_id,
            in_report.touch_1_0,
            determine_value=touch_1_active
        )
        self._handle_state(
            self._touch_1_x,
            calc_touch_x,
            in_report.touch_1_2,
            in_report.touch_1_1,
            determine_value=touch_1_active
        )
        self._handle_state(
            self._touch_1_y,
            calc_touch_x,
            in_report.touch_1_3,
            in_report.touch_1_2,
            determine_value=touch_1_active
        )

        # ##### TRIGGER FEEDBACK #####
        self._handle_state(self._l2_feedback_active, bool(in_report.l2_feedback & 0x10))
        self._handle_state(self._l2_feedback_value, in_report.l2_feedback & 0xff)
        self._handle_state(self._r2_feedback_active, bool(in_report.r2_feedback & 0x10))
        self._handle_state(self._r2_feedback_value, in_report.r2_feedback & 0xff)

        # ##### BATTERY #####
        self._handle_state(self._battery_level_percent, in_report.battery_0)
        self._handle_state(self._battery_full, not not (in_report.battery_0 & 0x20))
        self._handle_state(self._battery_charging, not not (in_report.battery_1 & 0x08))

    def on_change(self, name_or_callback: ReadStateName | AnyStateChangeCallback, callback: StateChangeCallback = None):
        if callback is None:
            self.on_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).on_change(callback)

    def on_any_change(self, callback: AnyStateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.on_change(callback)

    def remove_change_listener(
            self, name_or_callback: ReadStateName | AnyStateChangeCallback, callback: StateChangeCallback = None
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

    def remove_any_change_listener(self, callback: AnyStateChangeCallback) -> None:
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
