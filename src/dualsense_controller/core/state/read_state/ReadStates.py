import math
import time
from functools import partial
from typing import Any, Final
from typing import Callable

import pyee

from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.report.in_report import InReport
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.mapping.enum import StateValueMapping
from dualsense_controller.core.state.mapping.typedef import MapFn
from dualsense_controller.core.state.read_state.ReadState import ReadState
from dualsense_controller.core.state.read_state.ValueCalc import ValueCalc
from dualsense_controller.core.state.read_state.ValueCompare import ValueCompare
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Feedback, Gyroscope, JoyStick, \
    Orientation, \
    TouchFinger
from dualsense_controller.core.state.typedef import CompareFn, StateChangeCallback, StateValueFn, \
    StateValueType


class ReadStates:
    _EVENT_UPDATE: Final[str] = '_EVENT_UPDATE'

    def __init__(
            self,
            state_value_mapper: StateValueMapper = StateValueMapping.DEFAULT,
            enforce_update: bool = False,
            trigger_change_after_all_values_set: bool = True,
    ):
        # CONST
        self._states_dict: Final[dict[ReadStateName, ReadState]] = {}
        self._state_value_mapper: Final[StateValueMapper] = state_value_mapper
        self._trigger_change_after_all_values_set: Final[bool] = trigger_change_after_all_values_set
        self._states_to_trigger_after_all_states_set: Final[list[ReadState]] = []
        # VAR
        self._timestamp: int | None = None
        self._in_report: InReport | None = None
        self._update_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()

        # INIT STICKS
        self.left_stick_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_x_mapped_to_raw,
        )
        self.left_stick_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_y_mapped_to_raw,
        )
        self.left_stick: Final[ReadState[JoyStick]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK,
            enforce_update=enforce_update,
            default_value=JoyStick(),
            depends_on=[self.left_stick_x, self.left_stick_y],
            compare_fn=ValueCompare.compare_joystick,
            deadzone=self._state_value_mapper.left_stick_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_mapped_to_raw,
        )
        self.right_stick_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_x_mapped_to_raw,
        )
        self.right_stick_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y,
            enforce_update=enforce_update,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_y_mapped_to_raw,
        )
        self.right_stick: Final[ReadState[JoyStick]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK,
            enforce_update=enforce_update,
            default_value=JoyStick(),
            depends_on=[self.right_stick_x, self.right_stick_y],
            compare_fn=ValueCompare.compare_joystick,
            deadzone=self._state_value_mapper.right_stick_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_mapped_to_raw,
        )

        # INIT GYRO, ACCEL, ORIENT
        self.gyroscope_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_X,
            enforce_update=enforce_update,
        )
        self.gyroscope_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Y,
            enforce_update=enforce_update,
        )
        self.gyroscope_z: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Z,
            enforce_update=enforce_update,
        )
        self.gyroscope: Final[ReadState[Gyroscope]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE,
            enforce_update=enforce_update,
            default_value=Gyroscope(),
            depends_on=[self.gyroscope_x, self.gyroscope_y, self.gyroscope_z],
            compare_fn=ValueCompare.compare_gyroscope,
            threshold=state_value_mapper.gyroscope_threshold,
        )
        self.accelerometer_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_X,
            enforce_update=enforce_update,
        )
        self.accelerometer_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Y,
            enforce_update=enforce_update,
        )
        self.accelerometer_z: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Z,
            enforce_update=enforce_update,
        )
        self.accelerometer: Final[ReadState[Accelerometer]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER,
            enforce_update=enforce_update,
            default_value=Accelerometer(),
            depends_on=[self.accelerometer_x, self.accelerometer_y, self.accelerometer_z],
            compare_fn=ValueCompare.compare_accelerometer,
            threshold=state_value_mapper.accelerometer_threshold,
        )
        self.orientation: Final[ReadState[Orientation]] = self._create_and_register_state(
            ReadStateName.ORIENTATION,
            enforce_update=enforce_update,
            default_value=Orientation(0, 0, 0),
            depends_on=[self.accelerometer],
            compare_fn=ValueCompare.compare_orientation,
            threshold=state_value_mapper.orientation_threshold,
            raw_to_mapped_fn=lambda raw: Orientation(
                round(math.degrees(raw.pitch), 2),
                round(math.degrees(raw.roll), 2)
            ),
        )

        # INIT TRIGGERS
        self.l2: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.L2,
            enforce_update=enforce_update,
            compare_fn=ValueCompare.compare_trigger,
            deadzone=self._state_value_mapper.left_trigger_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.left_trigger_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_trigger_mapped_to_raw,
        )
        self.r2: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.R2,
            enforce_update=enforce_update,
            compare_fn=ValueCompare.compare_trigger,
            deadzone=self._state_value_mapper.right_trigger_deadzone_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.right_trigger_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_trigger_mapped_to_raw,
        )

        # INIT DIG BTN
        self.dpad: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.DPAD,
            enforce_update=enforce_update,
        )
        self.btn_up: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_UP,
            enforce_update=enforce_update,
            depends_on=[self.dpad],
        )
        self.btn_left: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_LEFT,
            enforce_update=enforce_update,
            depends_on=[self.dpad],
        )
        self.btn_down: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_DOWN,
            enforce_update=enforce_update,
            depends_on=[self.dpad],
        )
        self.btn_right: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_RIGHT,
            enforce_update=enforce_update,
            depends_on=[self.dpad],
        )

        self.btn_square: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_SQUARE,
            enforce_update=enforce_update,
        )
        self.btn_cross: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CROSS,
            enforce_update=enforce_update,
        )
        self.btn_circle: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CIRCLE,
            enforce_update=enforce_update,
        )
        self.btn_triangle: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TRIANGLE,
            enforce_update=enforce_update,
        )
        self.btn_l1: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L1,
            enforce_update=enforce_update,
        )
        self.btn_r1: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R1,
            enforce_update=enforce_update,
        )
        self.btn_l2: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L2,
            enforce_update=enforce_update,
        )
        self.btn_r2: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R2,
            enforce_update=enforce_update,
        )
        self.btn_create: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CREATE,
            enforce_update=enforce_update,
        )
        self.btn_options: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_OPTIONS,
            enforce_update=enforce_update,
        )
        self.btn_l3: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L3,
            enforce_update=enforce_update,
        )
        self.btn_r3: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R3,
            enforce_update=enforce_update,
        )
        self.btn_ps: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_PS,
            enforce_update=enforce_update,
        )
        self.btn_touchpad: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TOUCHPAD,
            enforce_update=enforce_update,
        )
        self.btn_mute: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_MUTE,
            enforce_update=enforce_update,
        )

        # INIT TOUCH
        self.touch_finger_1_active: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_ACTIVE,
            enforce_update=enforce_update,
        )
        self.touch_finger_1_id: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_ID,
            enforce_update=enforce_update,
        )
        self.touch_finger_1_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_X,
            enforce_update=enforce_update,
        )
        self.touch_finger_1_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_Y,
            enforce_update=enforce_update,
        )
        self.touch_finger_1: Final[ReadState[TouchFinger]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1,
            enforce_update=enforce_update,
            compare_fn=ValueCompare.compare_touch_finger,
            depends_on=[
                self.touch_finger_1_active,
                self.touch_finger_1_id,
                self.touch_finger_1_x,
                self.touch_finger_1_y
            ]
        )

        self.touch_finger_2_active: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_ACTIVE,
            enforce_update=enforce_update,
        )
        self.touch_finger_2_id: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_ID,
            enforce_update=enforce_update,
        )
        self.touch_finger_2_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_X,
            enforce_update=enforce_update,
        )
        self.touch_finger_2_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_Y,
            enforce_update=enforce_update,
        )
        self.touch_finger_2: Final[ReadState[TouchFinger]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2,
            enforce_update=enforce_update,
            compare_fn=ValueCompare.compare_touch_finger,
            depends_on=[
                self.touch_finger_2_active,
                self.touch_finger_2_id,
                self.touch_finger_2_x,
                self.touch_finger_2_y
            ]
        )

        # INIT FEEDBACK
        self.l2_feedback_active: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_ACTIVE,
            enforce_update=enforce_update,
        )
        self.l2_feedback_value: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK_VALUE,
            enforce_update=enforce_update,
        )
        self.l2_feedback: Final[ReadState[Feedback]] = self._create_and_register_state(
            ReadStateName.L2_FEEDBACK,
            enforce_update=enforce_update,
            depends_on=[self.l2_feedback_active, self.l2_feedback_value],
            compare_fn=ValueCompare.compare_feedback
        )

        self.r2_feedback_active: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_ACTIVE,
            enforce_update=enforce_update,
        )
        self.r2_feedback_value: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK_VALUE,
            enforce_update=enforce_update,
        )
        self.r2_feedback: Final[ReadState[Feedback]] = self._create_and_register_state(
            ReadStateName.R2_FEEDBACK,
            enforce_update=enforce_update,
            depends_on=[self.r2_feedback_active, self.r2_feedback_value],
            compare_fn=ValueCompare.compare_feedback
        )

        # INIT BATT
        self.battery_level_percentage: Final[ReadState[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT,
            enforce_update=enforce_update,
            ignore_none=False,
        )
        self.battery_full: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL,
            enforce_update=enforce_update,
            ignore_none=False,
        )
        self.battery_charging: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING,
            enforce_update=enforce_update,
            ignore_none=False,
        )
        self.battery: Final[ReadState[Battery]] = self._create_and_register_state(
            ReadStateName.BATTERY,
            enforce_update=enforce_update,
            ignore_none=False,
            depends_on=[self.battery_level_percentage, self.battery_full, self.battery_charging],
            compare_fn=ValueCompare.compare_battery
        )

    # #################### PRIVATE #######################

    def _create_and_register_state(
            self,
            name: ReadStateName,
            value: StateValueType = None,
            default_value: StateValueType = None,
            ignore_none: bool = True,
            compare_fn: CompareFn[StateValueType] = None,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            depends_on: list[ReadState[Any]] = None,
            is_dependency_of: list[ReadState[Any]] = None,
            enforce_update: bool = False,
            **kwargs
    ) -> ReadState[StateValueType]:
        state: ReadState[StateValueType] = ReadState[StateValueType](
            name,
            value=value,
            default_value=default_value,
            mapped_to_raw_fn=mapped_to_raw_fn,
            raw_to_mapped_fn=raw_to_mapped_fn,
            compare_fn=partial(compare_fn, **kwargs) if compare_fn is not None else None,
            ignore_none=ignore_none,
            depends_on=depends_on,
            is_dependency_of=is_dependency_of,
            enforce_update=enforce_update
        )
        self._states_dict[name] = state
        return state

    def _get_state_by_name(self, name: ReadStateName) -> ReadState:
        return self._states_dict[name]

    def _handle_state(
            self,
            state: ReadState[StateValueType],
            value_or_value_fn: StateValueType | StateValueFn,
            *args,
            **kwagrs,
    ) -> StateValueType | None:
        state.set_cycle_timestamp(self._timestamp)
        if (
                state.enforce_update
                or state.has_listeners
                or state.has_listened_dependents
                or state.has_changed_dependencies
        ):
            value: StateValueType = value_or_value_fn if not callable(value_or_value_fn) else value_or_value_fn(
                self._in_report,
                *args,
                **kwagrs
            )
            if self._trigger_change_after_all_values_set:
                state.set_value_without_triggering_change(value)
                self._states_to_trigger_after_all_states_set.append(state)
            else:
                state.set_value(value)
            return value
        return None

    # #################### PUBLIC #######################

    def on_updated(self, callback: Callable[[], None]) -> None:
        self._update_emitter.on(self._EVENT_UPDATE, callback)

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        now_timestamp: int = time.perf_counter_ns()
        diff_timestamp: int = now_timestamp - self._timestamp if self._timestamp is not None else 0
        # print('diff_timestamp ns', diff_timestamp)

        self._timestamp = now_timestamp
        self._in_report = in_report

        # #### ANALOG STICKS #####

        self._handle_state(self.left_stick, ValueCalc.left_stick)
        # use values from stick because deadzone calc is done there
        self._handle_state(self.left_stick_x, ValueCalc.left_stick_x, self.left_stick)
        self._handle_state(self.left_stick_y, ValueCalc.left_stick_y, self.left_stick)

        self._handle_state(self.right_stick, ValueCalc.right_stick)
        # use values from stick because deadzone calc is done there
        self._handle_state(self.right_stick_x, ValueCalc.right_stick_x, self.right_stick)
        self._handle_state(self.right_stick_y, ValueCalc.right_stick_x, self.right_stick)

        # # ##### TRIGGERS #####
        self._handle_state(self.l2, ValueCalc.l2)
        self._handle_state(self.r2, ValueCalc.r2)
        #
        # # ##### BUTTONS #####
        self._handle_state(self.dpad, ValueCalc.dpad)
        self._handle_state(self.btn_up, ValueCalc.btn_up, self.dpad)
        self._handle_state(self.btn_down, ValueCalc.btn_down, self.dpad)
        self._handle_state(self.btn_left, ValueCalc.btn_left, self.dpad)
        self._handle_state(self.btn_right, ValueCalc.btn_right, self.dpad)

        self._handle_state(self.btn_cross, ValueCalc.btn_cross)
        self._handle_state(self.btn_r1, ValueCalc.btn_r1)
        self._handle_state(self.btn_square, ValueCalc.btn_square)
        self._handle_state(self.btn_circle, ValueCalc.btn_circle)
        self._handle_state(self.btn_triangle, ValueCalc.btn_triangle)
        self._handle_state(self.btn_l1, ValueCalc.btn_l1)
        self._handle_state(self.btn_l2, ValueCalc.btn_l2)
        self._handle_state(self.btn_r2, ValueCalc.btn_r2)
        self._handle_state(self.btn_create, ValueCalc.btn_create)
        self._handle_state(self.btn_options, ValueCalc.btn_options)
        self._handle_state(self.btn_l3, ValueCalc.btn_l3)
        self._handle_state(self.btn_r3, ValueCalc.btn_r3)
        self._handle_state(self.btn_ps, ValueCalc.btn_ps)
        self._handle_state(self.btn_mute, ValueCalc.btn_mute)
        self._handle_state(self.btn_touchpad, ValueCalc.btn_touchpad)

        # following not supported for BT01
        if connection_type == ConnectionType.BT_01:
            return

        # ##### GYRO #####

        self._handle_state(self.gyroscope, ValueCalc.gyroscope)
        self._handle_state(self.gyroscope_x, ValueCalc.gyroscope_x, self.gyroscope)
        self._handle_state(self.gyroscope_y, ValueCalc.gyroscope_y, self.gyroscope)
        self._handle_state(self.gyroscope_z, ValueCalc.gyroscope_z, self.gyroscope)
        #
        # ##### ACCEL #####
        self._handle_state(self.accelerometer, ValueCalc.accelerometer)
        self._handle_state(self.accelerometer_x, ValueCalc.accelerometer_x, self.accelerometer)
        self._handle_state(self.accelerometer_y, ValueCalc.accelerometer_y, self.accelerometer)
        self._handle_state(self.accelerometer_z, ValueCalc.accelerometer_z, self.accelerometer)
        #
        # ##### ORIENTATION #####
        self._handle_state(self.orientation, ValueCalc.orientation, self.accelerometer)
        #
        # ##### TOUCH 1 #####
        self._handle_state(self.touch_finger_1_active, ValueCalc.touch_finger_1_active)
        self._handle_state(self.touch_finger_1_id, ValueCalc.touch_finger_1_id)
        self._handle_state(self.touch_finger_1_x, ValueCalc.touch_finger_1_x)
        self._handle_state(self.touch_finger_1_y, ValueCalc.touch_finger_1_y)
        self._handle_state(
            self.touch_finger_1,
            ValueCalc.touch_finger_1,
            self.touch_finger_1_active,
            self.touch_finger_1_id,
            self.touch_finger_1_x,
            self.touch_finger_1_y
        )

        # ##### TOUCH 2 #####
        self._handle_state(self.touch_finger_2_active, ValueCalc.touch_finger_2_active)
        self._handle_state(self.touch_finger_2_id, ValueCalc.touch_finger_2_id)
        self._handle_state(self.touch_finger_2_x, ValueCalc.touch_finger_2_x)
        self._handle_state(self.touch_finger_2_y, ValueCalc.touch_finger_2_y)
        self._handle_state(
            self.touch_finger_2,
            ValueCalc.touch_finger_2,
            self.touch_finger_2_active,
            self.touch_finger_2_id,
            self.touch_finger_2_x,
            self.touch_finger_2_y
        )

        # ##### TRIGGER FEEDBACK INFO #####
        self._handle_state(self.l2_feedback_active, ValueCalc.l2_feedback_active)
        self._handle_state(self.l2_feedback_value, ValueCalc.l2_feedback_value)
        self._handle_state(
            self.l2_feedback,
            ValueCalc.l2_feedback,
            self.l2_feedback_active,
            self.l2_feedback_value
        )
        self._handle_state(self.r2_feedback_active, ValueCalc.r2_feedback_active)
        self._handle_state(self.r2_feedback_value, ValueCalc.r2_feedback_value)
        self._handle_state(
            self.r2_feedback,
            ValueCalc.r2_feedback,
            self.r2_feedback_active,
            self.r2_feedback_value
        )
        # ##### BATTERY #####
        self._handle_state(self.battery_level_percentage, ValueCalc.battery_level_percentage)
        self._handle_state(self.battery_full, ValueCalc.battery_full)
        self._handle_state(self.battery_charging, ValueCalc.battery_charging)
        self._handle_state(
            self.battery,
            ValueCalc.battery,
            self.battery_level_percentage,
            self.battery_full,
            self.battery_charging,
        )

        for state in self._states_to_trigger_after_all_states_set:
            state.trigger_change_if_changed()
        self._states_to_trigger_after_all_states_set.clear()

        self._update_emitter.emit(self._EVENT_UPDATE)

    def on_change(
            self, name_or_callback: ReadStateName | StateChangeCallback, callback: StateChangeCallback | None = None
    ):
        if callback is None:
            self.on_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).on_change(callback)

    def on_any_change(self, callback: StateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.on_change(callback)

    def remove_change_listener(
            self, name_or_callback: ReadStateName | StateChangeCallback, callback: StateChangeCallback | None = None
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

    def remove_any_change_listener(self, callback: StateChangeCallback) -> None:
        for state_name, state in self._states_dict.items():
            state.remove_change_listener(callback)
