import time
from typing import Callable, Final

from dualsense_controller import ConnectionType
from dualsense_controller.report import InReport
from dualsense_controller.state import (
    Accelerometer, AnyStateChangeCallback, BaseStates, Gyroscope, JoyStick,
    Orientation, ReadStateName, RestrictedStateAccess, State, StateChangeCallback,
    calc_accelerometer, calc_gyroscope, calc_orientation, calc_touch_id,
    calc_touch_x, calc_touch_y
)
from .common import StateDeterminationLevel, StateValueMapping, StateValueType, compare_accelerometer, \
    compare_gyroscope, \
    compare_joystick, \
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
            state_value_mapping: StateValueMapping = StateValueMapping.DEFAULT,
            state_determination: StateDeterminationLevel = StateDeterminationLevel.LISTENER,
            trigger_change_after_all_values_set: bool = True,
    ):
        super().__init__(
            state_value_mapping=state_value_mapping
        )
        # CONST
        self._state_determination_level: Final[StateDeterminationLevel] = state_determination
        self._trigger_change_after_all_values_set: Final[bool] = trigger_change_after_all_values_set
        self._states_to_trigger_after_all_states_set: Final[list[State]] = []
        # VAR
        self._update_timestamp: int | None = None

        # INIT STICKS
        self._left_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_x_mapped_to_raw,
        )
        self._left_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_y_mapped_to_raw,
        )
        self._left_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK,
            default_value=JoyStick(),
            is_based_on=[self._left_stick_x, self._left_stick_y],
            compare_fn=compare_joystick,
            deadzone=joystick_deadzone,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_mapped_to_raw,
        )
        self._right_stick_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_x_mapped_to_raw,
        )
        self._right_stick_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_y_mapped_to_raw,
        )
        self._right_stick: Final[State[JoyStick]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK,
            default_value=JoyStick(),
            is_based_on=[self._right_stick_x, self._right_stick_y],
            compare_fn=compare_joystick,
            deadzone=joystick_deadzone,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_mapped_to_raw,
        )

        # INIT GYRO, ACCEL, ORIENT
        self._gyroscope_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_X,
        )
        self._gyroscope_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Y,
        )
        self._gyroscope_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Z,
        )
        self._gyroscope: Final[State[Gyroscope]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE,
            default_value=Gyroscope(),
            is_based_on=[self._gyroscope_x, self._gyroscope_y, self._gyroscope_z],
            compare_fn=compare_gyroscope,
            threshold=gyroscope_threshold,
        )
        self._accelerometer_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_X,
        )
        self._accelerometer_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Y,
        )
        self._accelerometer_z: Final[State[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Z,
        )
        self._accelerometer: Final[State[Accelerometer]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER,
            default_value=Accelerometer(),
            is_based_on=[self._accelerometer_x, self._accelerometer_y, self._accelerometer_z],
            compare_fn=compare_accelerometer,
            threshold=accelerometer_threshold,
        )
        self._orientation: Final[State[Orientation]] = self._create_and_register_state(
            ReadStateName.ORIENTATION,
            default_value=Orientation(),
            is_based_on=[self._gyroscope, self._accelerometer],
            compare_fn=compare_orientation,
            threshold=orientation_threshold,
        )

        # INIT SHOULDER KEYS
        self._l2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2,
            compare_fn=compare_shoulder_key,
            deadzone=shoulder_key_deadzone,
            raw_to_mapped_fn=self._state_value_mapper.left_shoulder_key_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_shoulder_key_mapped_to_raw,
        )
        self._r2: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2,
            compare_fn=compare_shoulder_key,
            deadzone=shoulder_key_deadzone,
            raw_to_mapped_fn=self._state_value_mapper.right_shoulder_key_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_shoulder_key_mapped_to_raw,
        )

        # INIT DIG BTN
        self._btn_up: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_UP,
        )
        self._btn_left: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_LEFT,
        )
        self._btn_down: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_DOWN,
        )
        self._btn_right: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_RIGHT,
        )
        self._btn_square: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_SQUARE,
        )
        self._btn_cross: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CROSS,
        )
        self._btn_circle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CIRCLE,
        )
        self._btn_triangle: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TRIANGLE,
        )
        self._btn_l1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L1,
        )
        self._btn_r1: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R1,
        )
        self._btn_l2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L2,
        )
        self._btn_r2: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R2,
        )
        self._btn_create: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CREATE,
        )
        self._btn_options: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_OPTIONS,
        )
        self._btn_l3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L3,
        )
        self._btn_r3: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R3,
        )
        self._btn_ps: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_PS,
        )
        self._btn_touchpad: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TOUCHPAD,
        )
        self._btn_mute: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BTN_MUTE,
        )

        # INIT TOUCH
        self._touch_0_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ACTIVE,
        )
        self._touch_0_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_ID,
        )
        self._touch_0_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_X,
        )
        self._touch_0_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_0_Y,
        )
        self._touch_1_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ACTIVE,
        )
        self._touch_1_id: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_ID,
        )
        self._touch_1_x: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_X,
        )
        self._touch_1_y: Final[State[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_1_Y,
        )

        # INIT FEEDBACK
        self._l2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_ACTIVE,
        )
        self._l2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_VALUE,
        )
        self._r2_feedback_active: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_ACTIVE,
        )
        self._r2_feedback_value: Final[State[int]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_VALUE,
        )

        # INIT BATT
        self._battery_level_percent: Final[State[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT,
            ignore_none=False,
        )
        self._battery_full: Final[State[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL,
            ignore_none=False,
        )
        self._battery_charging: Final[State[int]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING,
            ignore_none=False,
        )

    # #################### PRIVATE #######################

    def _handle_state(
            self,
            state: State[StateValueType],
            value_or_calc_fn: StateValueType | Callable[[...], StateValueType],
            *args,
            skip: bool = False,
    ) -> StateValueType | None:
        if skip:
            return None
        if (
                self._state_determination_level == StateDeterminationLevel.ALWAYS
                or state.has_listeners
                or state.has_changed_deps
        ):
            value_: StateValueType = value_or_calc_fn(*args) if callable(value_or_calc_fn) else value_or_calc_fn
            if self._trigger_change_after_all_values_set:
                state.set_value_without_triggering_change(value_,self._update_timestamp)
                self._states_to_trigger_after_all_states_set.append(state,self._update_timestamp)
            else:
                state.value = value_
            return value_
        return None

    # #################### PUBLIC #######################

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        self._update_timestamp = int(time.time())

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

        self._handle_state(
            self._gyroscope, calc_gyroscope,
            in_report.gyro_x_1, in_report.gyro_x_0,
            in_report.gyro_y_1, in_report.gyro_y_0,
            in_report.gyro_z_1, in_report.gyro_z_0
        )
        self._handle_state(self._gyroscope_x, self._gyroscope.value.x)
        self._handle_state(self._gyroscope_y, self._gyroscope.value.y)
        self._handle_state(self._gyroscope_z, self._gyroscope.value.z)

        # ##### ACCEL #####
        self._handle_state(
            self._accelerometer, calc_accelerometer,
            in_report.accel_x_1, in_report.accel_x_0,
            in_report.accel_y_1, in_report.accel_y_0,
            in_report.accel_z_1, in_report.accel_z_0
        )
        self._handle_state(self._accelerometer_x, self._accelerometer.value.x)
        self._handle_state(self._accelerometer_y, self._accelerometer.value.y)
        self._handle_state(self._accelerometer_z, self._accelerometer.value.z)

        # ##### ORIENTATION #####
        self._handle_state(self._orientation, calc_orientation, self._gyroscope, self._accelerometer)

        # ##### TOUCH #####
        touch_0_active: bool = self._handle_state(self._touch_0_active, not (in_report.touch_0_0 & 0x80))
        self._handle_state(
            self._touch_0_id,
            calc_touch_id,
            in_report.touch_0_0,
            skip=not touch_0_active,
        )
        self._handle_state(
            self._touch_0_x,
            calc_touch_x,
            in_report.touch_0_2,
            in_report.touch_0_1,
            skip=not touch_0_active,
        )
        self._handle_state(
            self._touch_0_y,
            calc_touch_y,
            in_report.touch_0_3,
            in_report.touch_0_2,
            skip=not touch_0_active,
        )

        touch_1_active: bool = self._handle_state(self._touch_1_active, not (in_report.touch_1_0 & 0x80))
        self._handle_state(
            self._touch_1_id,
            calc_touch_id,
            in_report.touch_1_0,
            skip=not touch_0_active,
        )
        self._handle_state(
            self._touch_1_x,
            calc_touch_x,
            in_report.touch_1_2,
            in_report.touch_1_1,
            skip=not touch_0_active,
        )
        self._handle_state(
            self._touch_1_y,
            calc_touch_x,
            in_report.touch_1_3,
            in_report.touch_1_2,
            skip=not touch_0_active,
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

        for state in self._states_to_trigger_after_all_states_set:
            state.trigger_change_if_changed()
        self._states_to_trigger_after_all_states_set.clear()

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
