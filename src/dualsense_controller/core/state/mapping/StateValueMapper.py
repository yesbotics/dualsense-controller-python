from functools import partial

from dualsense_controller.core.state.mapping.common import Float, FromTo, Integer, StateValueMappingData
from dualsense_controller.core.state.mapping.enum import StateValueMapping
from dualsense_controller.core.state.mapping.typedef import FromToTuple, MapFn
from dualsense_controller.core.state.read_state.value_type import JoyStick
from dualsense_controller.core.state.typedef import Number

_NumberType = Float | Integer


class StateValueMapper:

    @staticmethod
    def _number_map(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        if in_min == out_min and in_max == out_max:
            return value
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @classmethod
    def _number_raw_to_mapped(cls, from_to: FromTo | None, value: Number) -> Number:
        if from_to is None:
            return value
        to_type: _NumberType = from_to.to_type
        value_type: Number = to_type.value_type
        from_to_tuple: FromToTuple = from_to.as_tuple
        mapped_value: Number = value_type(cls._number_map(value, *from_to_tuple))
        if isinstance(mapped_value, float):
            mapped_value = round(mapped_value, to_type.round_digits)
        return mapped_value

    @classmethod
    def _number_mapped_to_raw(cls, from_to: FromTo, value: Number) -> Number:
        if from_to is None:
            return value
        raw_value: int = int(cls._number_map(value, *from_to.swapped.as_tuple))
        return raw_value

    @classmethod
    def _joystick_mapped_to_raw(cls, from_to: FromTo, value: JoyStick) -> JoyStick:
        return JoyStick(
            x=cls._number_mapped_to_raw(from_to, value.x),
            y=cls._number_mapped_to_raw(from_to, value.y)
        )

    @classmethod
    def _joystick_raw_to_mapped(
            cls,
            from_to_x: FromTo,
            from_to_y: FromTo,
            value: JoyStick,
    ) -> JoyStick:
        return JoyStick(
            x=cls._number_raw_to_mapped(from_to_x, value.x),
            y=cls._number_raw_to_mapped(from_to_y, value.y),
        )

    def __init__(
            self,
            mapping: StateValueMapping,
            left_joystick_deadzone: Number = 0,
            right_joystick_deadzone: Number = 0,
            l2_deadzone: Number = 0,
            r2_deadzone: Number = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
    ):

        self._mapping_data: StateValueMappingData = mapping.value
        if isinstance(self._mapping_data, tuple):
            self._mapping_data = self._mapping_data[0]

        if self._mapping_data is None:
            return

        # #################################################### DEADZONE AND THRESHOLD ###############################
        self.left_stick_deadzone_mapped_to_raw: Number = (
            left_joystick_deadzone if self._mapping_data is None else self._number_mapped_to_raw(
                self._mapping_data.left_stick_deadzone,
                left_joystick_deadzone
            )
        )
        self.right_stick_deadzone_mapped_to_raw: Number = (
            right_joystick_deadzone if self._mapping_data is None else self._number_mapped_to_raw(
                self._mapping_data.right_stick_deadzone,
                right_joystick_deadzone
            )
        )
        self.left_trigger_deadzone_mapped_to_raw: Number = (
            l2_deadzone if self._mapping_data is None else self._number_mapped_to_raw(
                self._mapping_data.l2_deadzone,
                l2_deadzone
            )
        )
        self.right_trigger_deadzone_mapped_to_raw: Number = (
            r2_deadzone if self._mapping_data is None else self._number_mapped_to_raw(
                self._mapping_data.r2_deadzone,
                r2_deadzone
            )
        )
        self.gyroscope_threshold: Number = (
            gyroscope_threshold if self._mapping_data is None else self._number_mapped_to_raw(
                self._mapping_data.r2_deadzone,
                gyroscope_threshold
            )
        )
        self.accelerometer_threshold: Number = (
            accelerometer_threshold if self._mapping_data is None else self._number_mapped_to_raw(
                self._mapping_data.r2_deadzone,
                accelerometer_threshold
            )
        )
        self.orientation_threshold: Number = (
            orientation_threshold if self._mapping_data is None else self._number_mapped_to_raw(
                self._mapping_data.r2_deadzone,
                orientation_threshold
            )
        )

        # #################################################### JOYSTICKS ###############################
        self.left_stick_x_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._number_raw_to_mapped,
            self._mapping_data.left_stick_x,
        )
        self.left_stick_x_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.left_stick_x
        )
        self.left_stick_y_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._number_raw_to_mapped,
            self._mapping_data.left_stick_y,
        )
        self.left_stick_y_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.left_stick_y
        )
        self.left_stick_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._joystick_raw_to_mapped,
            self._mapping_data.left_stick_x,
            self._mapping_data.left_stick_y,
        )
        self.left_stick_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._joystick_mapped_to_raw,
            self._mapping_data.left_stick_x,
            self._mapping_data.left_stick_y,
        )
        self.right_stick_x_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._number_raw_to_mapped,
            self._mapping_data.right_stick_x,
        )
        self.right_stick_x_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.right_stick_x
        )
        self.right_stick_y_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._number_raw_to_mapped,
            self._mapping_data.right_stick_y,
        )
        self.right_stick_y_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.right_stick_y
        )
        self.right_stick_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._joystick_raw_to_mapped,
            self._mapping_data.right_stick_x,
            self._mapping_data.right_stick_y,
        )
        self.right_stick_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._joystick_mapped_to_raw,
            self._mapping_data.right_stick_x,
            self._mapping_data.right_stick_y,
        )

        # #################################################### TRIGGERS ###############################
        self.left_trigger_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._number_raw_to_mapped,
            self._mapping_data.l2
        )
        self.left_trigger_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.l2
        )
        self.right_trigger_raw_to_mapped: MapFn | None = None if self._mapping_data is None else partial(
            self._number_raw_to_mapped,
            self._mapping_data.r2
        )
        self.right_trigger_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.r2
        )

        # #################################################### MOTORS - ONLY NEED TO SET ###############################
        self.set_left_motor_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.set_motor_left
        )
        self.set_right_motor_mapped_to_raw: MapFn | None = None if self._mapping_data is None else partial(
            self._number_mapped_to_raw,
            self._mapping_data.set_motor_right
        )
