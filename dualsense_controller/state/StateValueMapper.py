from functools import partial

from dualsense_controller.state import FromToTuple, JoyStick, MapFn, Number, StateValueMapping, StateValueMappingData


class StateValueMapper:

    @staticmethod
    def _number_map(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        if in_min == out_min and in_max == out_max:
            return value
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @classmethod
    def _number_raw_to_mapped(cls, from_to_tuple: FromToTuple, value: Number) -> Number:
        return StateValueMapper._number_map(value, *from_to_tuple)

    @classmethod
    def _number_mapped_to_raw(cls, from_to_tuple: FromToTuple, value: Number) -> Number:
        return int(StateValueMapper._number_map(value, *from_to_tuple.__reversed__()))

    @classmethod
    def _joystick_mapped_to_raw(cls, from_to_tuple: FromToTuple, value: JoyStick) -> JoyStick:
        return JoyStick(
            x=cls._number_mapped_to_raw(from_to_tuple, value.x),
            y=cls._number_mapped_to_raw(from_to_tuple, value.y),
        )

    @classmethod
    def _joystick_raw_to_mapped(cls, from_to_tuple_x: FromToTuple, from_to_tuple_y: FromToTuple,
                                value: JoyStick) -> JoyStick:
        return JoyStick(
            x=cls._number_raw_to_mapped(from_to_tuple_x, value.x),
            y=cls._number_raw_to_mapped(from_to_tuple_y, value.y),
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
