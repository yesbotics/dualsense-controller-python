import math
import time
from functools import partial
from typing import Any, Final
from typing import Callable

import pyee

from dualsense_controller.core.core.Lockable import Lockable
from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.report.in_report import InReport
from dualsense_controller.core.state.BaseStates import BaseStates
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.mapping.typedef import MapFn
from dualsense_controller.core.state.read_state.ReadState import ReadState
from dualsense_controller.core.state.read_state.ValueCalc import ValueCalc
from dualsense_controller.core.state.read_state.ValueCompare import ValueCompare
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Gyroscope, JoyStick, \
    Orientation, TouchFinger, TriggerFeedback, Trigger
from dualsense_controller.core.state.typedef import CompareFn, Number, StateValue, StateValueFn
from dualsense_controller.core.util import check_value_restrictions


class ReadStates(BaseStates):
    _EVENT_UPDATE: Final[str] = '_EVENT_UPDATE'

    def __init__(
            self,
            state_value_mapper: StateValueMapper,
            enforce_update: bool = False,
            can_update_itself: bool = True,
    ):
        super().__init__(state_value_mapper)
        # CONST
        self._states_to_trigger_after_all_states_set: Final[list[ReadState]] = []
        self._in_report_lockable: Final[Lockable[InReport]] = Lockable()
        # VAR
        self._timestamp: int | None = None
        self._update_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()

        # INIT STICKS
        self.left_stick: Final[ReadState[JoyStick]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK,
            in_report_lockable=self._in_report_lockable,
            value_calc_fn=ValueCalc.get_left_stick,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_joystick,
            deadzone_raw=self._state_value_mapper.left_stick_deadzone_mapped_to_raw,
            middle_deadzone=self._state_value_mapper.left_stick_deadzone_mapped,
            mapped_min_max_values=[
                (self._state_value_mapper.mapping_data.left_stick_x.to_min
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.left_stick_x is not None else 0),
                (self._state_value_mapper.mapping_data.left_stick_x.to_max
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.left_stick_x is not None else 255),
                (self._state_value_mapper.mapping_data.left_stick_y.to_min
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.left_stick_y is not None else 0),
                (self._state_value_mapper.mapping_data.left_stick_y.to_max
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.left_stick_y is not None else 255),
            ],
            raw_to_mapped_fn=self._state_value_mapper.left_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_mapped_to_raw,
        )
        self.left_stick_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_X,
            depends_on=[self.left_stick],
            value_calc_fn=ValueCalc.get_left_stick_x,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_x_mapped_to_raw,
        )
        self.left_stick_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.LEFT_STICK_Y,
            depends_on=[self.left_stick],
            value_calc_fn=ValueCalc.get_left_stick_y,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=self._state_value_mapper.left_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_stick_y_mapped_to_raw,
        )
        self.right_stick: Final[ReadState[JoyStick]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK,
            value_calc_fn=ValueCalc.get_right_stick,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_joystick,
            deadzone_raw=self._state_value_mapper.right_stick_deadzone_mapped_to_raw,
            middle_deadzone=self._state_value_mapper.right_stick_deadzone_mapped,
            mapped_min_max_values=[
                (self._state_value_mapper.mapping_data.right_stick_x.to_min
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.right_stick_x is not None else 0),
                (self._state_value_mapper.mapping_data.right_stick_x.to_max
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.right_stick_x is not None else 255),
                (self._state_value_mapper.mapping_data.right_stick_y.to_min
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.right_stick_y is not None else 0),
                (self._state_value_mapper.mapping_data.right_stick_y.to_max
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.right_stick_y is not None else 255),
            ],
            raw_to_mapped_fn=self._state_value_mapper.right_stick_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_mapped_to_raw,
        )
        self.right_stick_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_X,
            depends_on=[self.right_stick],
            value_calc_fn=ValueCalc.get_right_stick_x,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_x_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_x_mapped_to_raw,
        )
        self.right_stick_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_STICK_Y,
            depends_on=[self.right_stick],
            value_calc_fn=ValueCalc.get_right_stick_y,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=self._state_value_mapper.right_stick_y_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_stick_y_mapped_to_raw,
        )

        # GYRO
        self.gyroscope: Final[ReadState[Gyroscope]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE,
            value_calc_fn=ValueCalc.get_gyroscope,
            in_report_lockable=self._in_report_lockable,
            default_value=Gyroscope(),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_gyroscope,
            threshold_raw=state_value_mapper.gyroscope_threshold_mapped_to_raw,
            threshold=state_value_mapper.gyroscope_threshold_mapped,
        )
        self.gyroscope_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_X,
            depends_on=[self.gyroscope],
            value_calc_fn=ValueCalc.get_gyroscope_x,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.gyroscope_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Y,
            depends_on=[self.gyroscope],
            value_calc_fn=ValueCalc.get_gyroscope_y,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.gyroscope_z: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.GYROSCOPE_Z,
            depends_on=[self.gyroscope],
            value_calc_fn=ValueCalc.get_gyroscope_z,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        # ACCEL
        self.accelerometer: Final[ReadState[Accelerometer]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER,
            value_calc_fn=ValueCalc.get_accelerometer,
            in_report_lockable=self._in_report_lockable,
            default_value=Accelerometer(),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_accelerometer,
            threshold_raw=state_value_mapper.accelerometer_threshold_mapped_to_raw,
            threshold=state_value_mapper.accelerometer_threshold_mapped,
        )
        self.accelerometer_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_X,
            depends_on=[self.accelerometer],
            value_calc_fn=ValueCalc.get_accelerometer_x,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.accelerometer_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Y,
            depends_on=[self.accelerometer],
            value_calc_fn=ValueCalc.get_accelerometer_y,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.accelerometer_z: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.ACCELEROMETER_Z,
            depends_on=[self.accelerometer],
            value_calc_fn=ValueCalc.get_accelerometer_z,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        # ORIENT
        self.orientation: Final[ReadState[Orientation]] = self._create_and_register_state(
            ReadStateName.ORIENTATION,
            value_calc_fn=ValueCalc.get_orientation,
            in_report_lockable=self._in_report_lockable,
            default_value=Orientation(0, 0, 0),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=[self.accelerometer],
            compare_fn=ValueCompare.compare_orientation,
            threshold_raw=state_value_mapper.orientation_threshold_mapped_to_raw,
            threshold=state_value_mapper.orientation_threshold_mapped,
            raw_to_mapped_fn=lambda raw: Orientation(
                round(math.degrees(raw.pitch), 2),
                round(math.degrees(raw.roll), 2)
            ),
        )

        # INIT DIG BTN
        self.dpad: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.DPAD,
            value_calc_fn=ValueCalc.get_dpad,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_up: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_UP,
            value_calc_fn=ValueCalc.get_btn_up,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=[self.dpad],
        )
        self.btn_left: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_LEFT,
            value_calc_fn=ValueCalc.get_btn_left,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=[self.dpad],
        )
        self.btn_down: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_DOWN,
            value_calc_fn=ValueCalc.get_btn_down,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=[self.dpad],
        )
        self.btn_right: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_RIGHT,
            value_calc_fn=ValueCalc.get_btn_right,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=[self.dpad],
        )

        self.btn_square: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_SQUARE,
            value_calc_fn=ValueCalc.get_btn_square,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_cross: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CROSS,
            value_calc_fn=ValueCalc.get_btn_cross,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_circle: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CIRCLE,
            value_calc_fn=ValueCalc.get_btn_circle,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_triangle: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TRIANGLE,
            value_calc_fn=ValueCalc.get_btn_triangle,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_l1: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L1,
            value_calc_fn=ValueCalc.get_btn_l1,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_r1: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R1,
            value_calc_fn=ValueCalc.get_btn_r1,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_l2: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L2,
            value_calc_fn=ValueCalc.get_btn_l2,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_r2: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R2,
            value_calc_fn=ValueCalc.get_btn_r2,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_create: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_CREATE,
            value_calc_fn=ValueCalc.get_btn_create,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_options: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_OPTIONS,
            value_calc_fn=ValueCalc.btn_options,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_l3: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_L3,
            value_calc_fn=ValueCalc.get_btn_l3,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_r3: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_R3,
            value_calc_fn=ValueCalc.get_btn_r3,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_ps: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_PS,
            value_calc_fn=ValueCalc.get_btn_ps,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_touchpad: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_TOUCHPAD,
            value_calc_fn=ValueCalc.get_btn_touchpad,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_mute: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BTN_MUTE,
            value_calc_fn=ValueCalc.get_btn_mute,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        # INIT TOUCH
        self.touch_finger_1_active: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_ACTIVE,
            value_calc_fn=ValueCalc.get_touch_finger_1_active,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_1_id: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_ID,
            value_calc_fn=ValueCalc.get_touch_finger_1_id,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_1_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_X,
            value_calc_fn=ValueCalc.get_touch_finger_1_x,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_1_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1_Y,
            value_calc_fn=ValueCalc.get_touch_finger_1_y,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_1: Final[ReadState[TouchFinger]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_1,
            value_calc_fn=ValueCalc.get_touch_finger_1,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
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
            value_calc_fn=ValueCalc.get_touch_finger_2_active,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_2_id: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_ID,
            value_calc_fn=ValueCalc.get_touch_finger_2_id,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_2_x: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_X,
            value_calc_fn=ValueCalc.get_touch_finger_2_x,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_2_y: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2_Y,
            value_calc_fn=ValueCalc.get_touch_finger_2_y,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.touch_finger_2: Final[ReadState[TouchFinger]] = self._create_and_register_state(
            ReadStateName.TOUCH_FINGER_2,
            value_calc_fn=ValueCalc.get_touch_finger_2,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_touch_finger,
            depends_on=[
                self.touch_finger_2_active,
                self.touch_finger_2_id,
                self.touch_finger_2_x,
                self.touch_finger_2_y
            ]
        )

        # INIT TRIGGERS
        self.left_trigger_value: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.LEFT_TRIGGER_VALUE,
            value_calc_fn=ValueCalc.get_left_trigger_value,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_trigger_value,
            deadzone_raw=self._state_value_mapper.left_trigger_deadzone_mapped_to_raw,
            deadzone=self._state_value_mapper.left_trigger_deadzone_mapped,
            mapped_min_max_values=[
                (self._state_value_mapper.mapping_data.left_trigger.to_min
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.left_trigger is not None else 0),
                (self._state_value_mapper.mapping_data.left_trigger.to_max
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.left_trigger is not None else 255),
            ],
            raw_to_mapped_fn=self._state_value_mapper.left_trigger_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.left_trigger_mapped_to_raw,
        )
        self.left_trigger_feedback_active: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.LEFT_TRIGGER_FEEDBACK_ACTIVE,
            value_calc_fn=ValueCalc.get_left_trigger_feedback_active,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.left_trigger_feedback_value: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.LEFT_TRIGGER_FEEDBACK_VALUE,
            value_calc_fn=ValueCalc.get_left_trigger_feedback_value,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.left_trigger_feedback: Final[ReadState[TriggerFeedback]] = self._create_and_register_state(
            ReadStateName.LEFT_TRIGGER_FEEDBACK,
            value_calc_fn=ValueCalc.get_left_trigger_feedback,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=[self.left_trigger_feedback_active, self.left_trigger_feedback_value],
            compare_fn=ValueCompare.compare_trigger_feedback
        )

        self.right_trigger_value: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_TRIGGER_VALUE,
            value_calc_fn=ValueCalc.get_right_trigger_value,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_trigger_value,
            deadzone_raw=self._state_value_mapper.right_trigger_deadzone_mapped_to_raw,
            deadzone=self._state_value_mapper.right_trigger_deadzone_mapped,
            mapped_min_max_values=[
                (self._state_value_mapper.mapping_data.right_trigger.to_min
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.right_trigger is not None else 0),
                (self._state_value_mapper.mapping_data.right_trigger.to_max
                 if self._state_value_mapper.mapping_data is not None
                    and self._state_value_mapper.mapping_data.right_trigger is not None else 255),
            ],
            raw_to_mapped_fn=self._state_value_mapper.right_trigger_raw_to_mapped,
            mapped_to_raw_fn=self._state_value_mapper.right_trigger_mapped_to_raw,
        )
        self.right_trigger_feedback_active: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.RIGHT_TRIGGER_FEEDBACK_ACTIVE,
            value_calc_fn=ValueCalc.get_right_trigger_feedback_active,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.right_trigger_feedback_value: Final[ReadState[int]] = self._create_and_register_state(
            ReadStateName.RIGHT_TRIGGER_FEEDBACK_VALUE,
            value_calc_fn=ValueCalc.get_right_trigger_feedback_value,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.right_trigger_feedback: Final[ReadState[TriggerFeedback]] = self._create_and_register_state(
            ReadStateName.RIGHT_TRIGGER_FEEDBACK,
            value_calc_fn=ValueCalc.get_right_trigger_feedback,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=[self.right_trigger_feedback_active, self.right_trigger_feedback_value],
            compare_fn=ValueCompare.compare_trigger_feedback
        )

        # INIT BATT
        self.battery_level_percentage: Final[ReadState[float]] = self._create_and_register_state(
            ReadStateName.BATTERY_LEVEL_PERCENT,
            value_calc_fn=ValueCalc.get_battery_level_percentage,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            ignore_none=False,
        )
        self.battery_full: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_FULL,
            value_calc_fn=ValueCalc.get_battery_full,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            ignore_none=False,
        )
        self.battery_charging: Final[ReadState[bool]] = self._create_and_register_state(
            ReadStateName.BATTERY_CHARGING,
            value_calc_fn=ValueCalc.battery_charging,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            ignore_none=False,
        )
        self.battery: Final[ReadState[Battery]] = self._create_and_register_state(
            ReadStateName.BATTERY,
            value_calc_fn=ValueCalc.get_battery,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            ignore_none=False,
            depends_on=[self.battery_level_percentage, self.battery_full, self.battery_charging],
            compare_fn=ValueCompare.compare_battery
        )

    # #################### PRIVATE #######################

    def _create_and_register_state(
            self,

            # BASE
            name: ReadStateName,
            value: StateValue = None,
            default_value: StateValue = None,
            ignore_none: bool = True,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn[StateValue] = None,

            # READ STATES
            value_calc_fn: StateValueFn = None,
            in_report_lockable: Lockable[InReport] = None,
            enforce_update: bool = False,
            can_update_itself: bool = True,
            depends_on: list[ReadState[Any]] = None,
            is_dependency_of: list[ReadState[Any]] = None,
            mapped_min_max_values: list[Number] = None,
            middle_deadzone: Number = None,
            deadzone: Number = None,
            threshold: int = None,
            **kwargs
    ) -> ReadState[StateValue]:

        check_value_restrictions(
            name=str(name),
            mapped_min_max_values=mapped_min_max_values,
            middle_deadzone=middle_deadzone,
            deadzone=deadzone,
            threshold=threshold,
        )

        state: ReadState[StateValue] = ReadState[StateValue](
            # BASE
            name=name,
            value=value,
            default_value=default_value,
            ignore_none=ignore_none,
            mapped_to_raw_fn=mapped_to_raw_fn,
            raw_to_mapped_fn=raw_to_mapped_fn,
            compare_fn=partial(compare_fn, **kwargs) if compare_fn is not None else None,
            # READ STATE
            enforce_update=enforce_update,
            value_calc_fn=value_calc_fn,
            can_update_itself=can_update_itself,
            in_report_lockable=in_report_lockable,
            depends_on=depends_on,
            is_dependency_of=is_dependency_of,
        )
        self._register_state(name, state)
        return state

    def _handle_state(
            self,
            state: ReadState[StateValue],
    ) -> None:
        state.set_cycle_timestamp(self._timestamp)
        if state.is_updatable_from_outside:
            state.calc_value(trigger_change_on_changed=False)
            self._states_to_trigger_after_all_states_set.append(state)

    def _post_update(self):
        self._update_emitter.emit(self._EVENT_UPDATE)
        for state in self._states_to_trigger_after_all_states_set:
            state.trigger_change_if_changed()
        self._states_to_trigger_after_all_states_set.clear()

    # #################### PUBLIC #######################

    def on_updated(self, callback: Callable[[], None]) -> None:
        self._update_emitter.on(self._EVENT_UPDATE, callback)

    def once_updated(self, callback: Callable[[], None]) -> None:
        self._update_emitter.once(self._EVENT_UPDATE, callback)

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        now_timestamp: int = time.perf_counter_ns()
        diff_timestamp: int = now_timestamp - self._timestamp if self._timestamp is not None else 0
        # print('diff_timestamp ns', diff_timestamp)

        self._timestamp = now_timestamp
        self._in_report_lockable.value = in_report

        # #### ANALOG STICKS #####

        self._handle_state(self.left_stick)
        # use values from stick because deadzone_raw calc is done there
        self._handle_state(self.left_stick_x)
        self._handle_state(self.left_stick_y)

        self._handle_state(self.right_stick)
        # use values from stick because deadzone_raw calc is done there
        self._handle_state(self.right_stick_x)
        self._handle_state(self.right_stick_y)

        # # ##### TRIGGERS #####
        self._handle_state(self.left_trigger_value)
        self._handle_state(self.right_trigger_value)
        #
        # # ##### BUTTONS #####
        self._handle_state(self.dpad)
        self._handle_state(self.btn_up)
        self._handle_state(self.btn_down)
        self._handle_state(self.btn_left)
        self._handle_state(self.btn_right)

        self._handle_state(self.btn_cross)
        self._handle_state(self.btn_r1)
        self._handle_state(self.btn_square)
        self._handle_state(self.btn_circle)
        self._handle_state(self.btn_triangle)
        self._handle_state(self.btn_l1)
        self._handle_state(self.btn_l2)
        self._handle_state(self.btn_r2)
        self._handle_state(self.btn_create)
        self._handle_state(self.btn_options)
        self._handle_state(self.btn_l3)
        self._handle_state(self.btn_r3)
        self._handle_state(self.btn_ps)
        self._handle_state(self.btn_mute)
        self._handle_state(self.btn_touchpad)

        # following not supported for BT01
        if connection_type == ConnectionType.BT_01:
            self._post_update()
            return

        # ##### GYRO #####

        self._handle_state(self.gyroscope)
        self._handle_state(self.gyroscope_x)
        self._handle_state(self.gyroscope_y)
        self._handle_state(self.gyroscope_z)
        #
        # ##### ACCEL #####
        self._handle_state(self.accelerometer)
        self._handle_state(self.accelerometer_x)
        self._handle_state(self.accelerometer_y)
        self._handle_state(self.accelerometer_z)
        #
        # ##### ORIENTATION #####
        self._handle_state(self.orientation)
        #
        # ##### TOUCH 1 #####
        self._handle_state(self.touch_finger_1_active)
        self._handle_state(self.touch_finger_1_id)
        self._handle_state(self.touch_finger_1_x)
        self._handle_state(self.touch_finger_1_y)
        self._handle_state(self.touch_finger_1)

        # ##### TOUCH 2 #####
        self._handle_state(self.touch_finger_2_active)
        self._handle_state(self.touch_finger_2_id)
        self._handle_state(self.touch_finger_2_x)
        self._handle_state(self.touch_finger_2_y)
        self._handle_state(self.touch_finger_2)

        # ##### TRIGGER FEEDBACK INFO #####
        self._handle_state(self.left_trigger_feedback_active)
        self._handle_state(self.left_trigger_feedback_value)
        self._handle_state(self.left_trigger_feedback)
        self._handle_state(self.right_trigger_feedback_active)
        self._handle_state(self.right_trigger_feedback_value)
        self._handle_state(self.right_trigger_feedback)
        # ##### BATTERY #####
        self._handle_state(self.battery_level_percentage)
        self._handle_state(self.battery_full)
        self._handle_state(self.battery_charging)
        self._handle_state(self.battery)
        self._post_update()
