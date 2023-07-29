from functools import partial

from dualsense_controller.state import (
    Float, FromTo, FromToTuple,
    Integer, JoyStick,
    MapFn,
    Number,
    NumberType, StateValueMapping,
    StateValueMappingData
)


class StateValueMapper:

    @staticmethod
    def _number_map(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        if in_min == out_min and in_max == out_max:
            return value
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @classmethod
    def _number_raw_to_mapped(cls, from_to: FromTo, value: Number) -> Number:
        to_type: NumberType = from_to.to_type
        value_type: Number = to_type.value_type
        mapped_value: Number = value_type(cls._number_map(value, *from_to.as_tuple))
        if isinstance(mapped_value, float):
            mapped_value = round(mapped_value, to_type.round_digits)
        return mapped_value

    @classmethod
    def _number_mapped_to_raw(cls, from_to: FromTo, value: Number) -> Number:
        return from_to.from_type(cls._number_map(value, *from_to.reversed.as_tuple))

    @classmethod
    def _joystick_mapped_to_raw(cls, from_to: FromTo, value: JoyStick) -> JoyStick:
        return JoyStick(x=cls._number_mapped_to_raw(from_to, value.x), y=cls._number_mapped_to_raw(from_to, value.y))

    @classmethod
    def _joystick_raw_to_mapped(cls, from_to_x: FromTo, from_to_y: FromTo, value: JoyStick) -> JoyStick:
        return JoyStick(
            x=cls._number_raw_to_mapped(from_to_x, value.x),
            y=cls._number_raw_to_mapped(from_to_y, value.y),
        )

    def __init__(self, mapping: StateValueMapping):

        self.left_stick_x_raw_to_mapped: MapFn | None = None
        self.left_stick_x_mapped_to_raw: MapFn | None = None
        self.left_stick_y_raw_to_mapped: MapFn | None = None
        self.left_stick_y_mapped_to_raw: MapFn | None = None
        self.left_stick_raw_to_mapped: MapFn | None = None
        self.left_stick_mapped_to_raw: MapFn | None = None
        self.right_stick_x_raw_to_mapped: MapFn | None = None
        self.right_stick_x_mapped_to_raw: MapFn | None = None
        self.right_stick_y_raw_to_mapped: MapFn | None = None
        self.right_stick_y_mapped_to_raw: MapFn | None = None
        self.right_stick_raw_to_mapped: MapFn | None = None
        self.right_stick_mapped_to_raw: MapFn | None = None
        self.left_shoulder_key_raw_to_mapped: MapFn | None = None
        self.left_shoulder_key_mapped_to_raw: MapFn | None = None
        self.right_shoulder_key_raw_to_mapped: MapFn | None = None
        self.right_shoulder_key_mapped_to_raw: MapFn | None = None

        self._mapping_data: StateValueMappingData = mapping.value
        if isinstance(self._mapping_data, tuple):
            self._mapping_data = self._mapping_data[0]

        if self._mapping_data is None:
            return

        ######## LEFT JOYSTICK ##########
        self.left_stick_x_raw_to_mapped: MapFn = partial(
            self._number_raw_to_mapped,
            self._mapping_data.left_stick_x
        )
        self.left_stick_x_mapped_to_raw: MapFn = partial(
            self._number_mapped_to_raw,
            self._mapping_data.left_stick_x
        )
        self.left_stick_y_raw_to_mapped: MapFn = partial(
            self._number_raw_to_mapped,
            self._mapping_data.left_stick_y
        )
        self.left_stick_y_mapped_to_raw: MapFn = partial(
            self._number_mapped_to_raw,
            self._mapping_data.left_stick_y
        )
        self.left_stick_raw_to_mapped: MapFn = partial(
            self._joystick_raw_to_mapped,
            self._mapping_data.left_stick_x,
            self._mapping_data.left_stick_y,
        )
        self.left_stick_mapped_to_raw: MapFn = partial(
            self._joystick_mapped_to_raw,
            self._mapping_data.left_stick_x,
            self._mapping_data.left_stick_y,
        )

        ######## RIGHT JOYSTICK ##########
        self.right_stick_x_raw_to_mapped: MapFn = partial(
            self._number_raw_to_mapped,
            self._mapping_data.right_stick_x
        )
        self.right_stick_x_mapped_to_raw: MapFn = partial(
            self._number_mapped_to_raw,
            self._mapping_data.right_stick_x
        )
        self.right_stick_y_raw_to_mapped: MapFn = partial(
            self._number_raw_to_mapped,
            self._mapping_data.right_stick_y
        )
        self.right_stick_y_mapped_to_raw: MapFn = partial(
            self._number_mapped_to_raw,
            self._mapping_data.right_stick_y
        )
        self.right_stick_raw_to_mapped: MapFn = partial(
            self._joystick_raw_to_mapped,
            self._mapping_data.right_stick_x,
            self._mapping_data.right_stick_y,
        )
        self.right_stick_mapped_to_raw: MapFn = partial(
            self._joystick_mapped_to_raw,
            self._mapping_data.right_stick_x,
            self._mapping_data.right_stick_y,
        )

        self.left_shoulder_key_raw_to_mapped: MapFn = partial(
            self._number_raw_to_mapped,
            self._mapping_data.left_shoulder_key
        )
        self.left_shoulder_key_mapped_to_raw: MapFn = partial(
            self._number_mapped_to_raw,
            self._mapping_data.left_shoulder_key
        )

        self.right_shoulder_key_raw_to_mapped: MapFn = partial(
            self._number_raw_to_mapped,
            self._mapping_data.right_shoulder_key
        )
        self.right_shoulder_key_mapped_to_raw: MapFn = partial(
            self._number_mapped_to_raw,
            self._mapping_data.right_shoulder_key
        )
