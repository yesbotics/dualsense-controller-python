import functools

from dualsense_controller.state import FromToTuple, MapFn, Number, StateValueMapping, StateValueMappingData


class StateValueMapper:

    @staticmethod
    def _map(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        if in_min == out_min and in_max == out_max:
            return value
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @classmethod
    def _raw_to_mapped_inner(cls, from_to_tuple: FromToTuple, value: Number) -> Number:
        return StateValueMapper._map(value, *from_to_tuple)

    @classmethod
    def _mapped_to_raw_inner(cls, from_to_tuple: FromToTuple, value: Number) -> Number:
        return int(StateValueMapper._map(value, *from_to_tuple.__reversed__()))

    @classmethod
    def _mapped_to_raw(cls, from_to_tuple: FromToTuple) -> Number:
        return functools.partial(cls._mapped_to_raw_inner, from_to_tuple)

    @classmethod
    def _raw_to_mapped(cls, from_to_tuple: FromToTuple) -> Number:
        return functools.partial(cls._raw_to_mapped_inner, from_to_tuple)

    def __init__(self, mapping: StateValueMapping):
        self._mapping_data: StateValueMappingData = mapping.value
        if isinstance(self._mapping_data, tuple):
            self._mapping_data = self._mapping_data[0]

        self.left_stick_x_from_raw: MapFn = self._raw_to_mapped(self._mapping_data.left_stick_x)
        self.left_stick_x_to_raw: MapFn = self._mapped_to_raw(self._mapping_data.left_stick_x)
        self.left_stick_y_from_raw: MapFn = self._raw_to_mapped(self._mapping_data.left_stick_y)
        self.left_stick_y_to_raw: MapFn = self._mapped_to_raw(self._mapping_data.left_stick_y)

        self.right_stick_x_from_raw: MapFn = self._raw_to_mapped(self._mapping_data.right_stick_x)
        self.right_stick_x_to_raw: MapFn = self._mapped_to_raw(self._mapping_data.right_stick_x)
        self.right_stick_y_from_raw: MapFn = self._raw_to_mapped(self._mapping_data.right_stick_y)
        self.right_stick_y_to_raw: MapFn = self._mapped_to_raw(self._mapping_data.right_stick_y)

        self.left_shoulder_key_from_raw: MapFn = self._raw_to_mapped(self._mapping_data.left_shoulder_key)
        self.left_shoulder_key_to_raw: MapFn = self._mapped_to_raw(self._mapping_data.left_shoulder_key)

        self.right_shoulder_key_from_raw: MapFn = self._raw_to_mapped(self._mapping_data.right_shoulder_key)
        self.right_shoulder_key_to_raw: MapFn = self._mapped_to_raw(self._mapping_data.right_shoulder_key)
