from __future__ import annotations

from dataclasses import dataclass

from dualsense_controller.core.state.mapping.typedef import FromToTuple
from dualsense_controller.core.state.typedef import Number


@dataclass(frozen=True, slots=True)
class Integer:
    value_type: type[Number] = int


@dataclass(frozen=True, slots=True)
class Float:
    value_type: type[Number] = float
    round_digits: int = 2


@dataclass(frozen=True, slots=True)
class FromTo:
    from_min: int
    from_max: int
    to_min: Number
    to_max: Number
    from_type: Integer | Float = Integer()
    to_type: Integer | Float = Integer()

    @property
    def swapped(self) -> FromTo:
        return FromTo(self.to_min, self.to_max, self.from_min, self.from_max, self.to_type, self.from_type)

    @property
    def as_tuple(self) -> FromToTuple:
        return self.from_min, self.from_max, self.to_min, self.to_max


@dataclass(frozen=True, slots=True)
class StateValueMappingData:
    left_stick_x: FromTo = None
    left_stick_y: FromTo = None
    left_stick_deadzone: FromTo = None

    right_stick_x: FromTo = None
    right_stick_y: FromTo = None
    right_stick_deadzone: FromTo = None

    left_trigger: FromTo = None
    left_trigger_deadzone: FromTo = None

    right_trigger: FromTo = None
    right_trigger_deadzone: FromTo = None

    set_motor_left: FromTo = None
    set_motor_right: FromTo = None
