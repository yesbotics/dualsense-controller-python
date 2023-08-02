from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Final, TypeVar

from dualsense_controller import ConnectionType


class ReadStateName(str, Enum):
    DPAD = 'DPAD'

    BTN_UP = 'BTN_UP'
    BTN_LEFT = 'BTN_LEFT'
    BTN_DOWN = 'BTN_DOWN'
    BTN_RIGHT = 'BTN_RIGHT'

    BTN_SQUARE = "BTN_SQUARE"
    BTN_CROSS = "BTN_CROSS"
    BTN_CIRCLE = "BTN_CIRCLE"
    BTN_TRIANGLE = "BTN_TRIANGLE"
    BTN_L1 = "BTN_L1"
    BTN_R1 = "BTN_R1"
    BTN_L2 = "BTN_L2"
    BTN_R2 = "BTN_R2"
    BTN_CREATE = "BTN_CREATE"
    BTN_OPTIONS = "BTN_OPTIONS"
    BTN_L3 = "BTN_L3"
    BTN_R3 = "BTN_R3"
    BTN_PS = "BTN_PS"
    BTN_TOUCHPAD = "BTN_TOUCHPAD"
    BTN_MUTE = "BTN_MUTE"

    LEFT_STICK_X = 'LEFT_STICK_X'
    LEFT_STICK_Y = 'LEFT_STICK_Y'
    RIGHT_STICK_X = 'RIGHT_STICK_X'
    RIGHT_STICK_Y = 'RIGHT_STICK_Y'
    L2 = 'L2'
    R2 = 'R2'

    GYROSCOPE_X = "GYROSCOPE_X"
    GYROSCOPE_Y = "GYROSCOPE_Y"
    GYROSCOPE_Z = "GYROSCOPE_Z"
    ACCELEROMETER_X = "ACCELEROMETER_X"
    ACCELEROMETER_Y = "ACCELEROMETER_Y"
    ACCELEROMETER_Z = "ACCELEROMETER_Z"

    TOUCH_FINGER_1_ACTIVE = 'TOUCH_FINGER_1_ACTIVE'
    TOUCH_FINGER_1_ID = 'TOUCH_FINGER_1_ID'
    TOUCH_FINGER_1_X = 'TOUCH_FINGER_1_X'
    TOUCH_FINGER_1_Y = 'TOUCH_FINGER_1_Y'
    TOUCH_FINGER_2_ACTIVE = 'TOUCH_FINGER_2_ACTIVE'
    TOUCH_FINGER_2_ID = 'TOUCH_FINGER_2_ID'
    TOUCH_FINGER_2_X = 'TOUCH_FINGER_2_X'
    TOUCH_FINGER_2_Y = 'TOUCH_FINGER_2_Y'

    L2_FEEDBACK_ACTIVE = 'L2_FEEDBACK_ACTIVE'
    L2_FEEDBACK_VALUE = 'L2_FEEDBACK_VALUE'
    R2_FEEDBACK_ACTIVE = 'R2_FEEDBACK_ACTIVE'
    R2_FEEDBACK_VALUE = 'R2_FEEDBACK_VALUE'

    BATTERY_LEVEL_PERCENT = 'BATTERY_LEVEL_PERCENT'
    BATTERY_FULL = 'BATTERY_FULL'
    BATTERY_CHARGING = 'BATTERY_CHARGING'

    # COMPLEX
    LEFT_STICK = 'LEFT_STICK'
    RIGHT_STICK = 'RIGHT_STICK'
    GYROSCOPE = 'GYROSCOPE'
    ACCELEROMETER = 'ACCELEROMETER'
    ORIENTATION = 'ORIENTATION'
    TOUCH_FINGER_1 = 'TOUCH_FINGER_1'
    TOUCH_FINGER_2 = 'TOUCH_FINGER_2'
    L2_FEEDBACK = "L2_FEEDBACK"
    R2_FEEDBACK = "R2_FEEDBACK"
    BATTERY = "BATTERY"


class WriteStateName(str, Enum):
    FLAGS_LIGHTS = 'FLAGS_LIGHTS'
    FLAGS_PHYSICS = 'FLAGS_PHYSICS'
    LIGHTBAR_RED = 'LIGHTBAR_RED'
    LIGHTBAR_GREEN = 'LIGHTBAR_GREEN'
    LIGHTBAR_BLUE = 'LIGHTBAR_BLUE'
    MOTOR_LEFT = 'MOTOR_LEFT'
    MOTOR_RIGHT = 'MOTOR_RIGHT'
    L2_EFFECT_MODE = 'L2_EFFECT_MODE'
    L2_EFFECT_PARAM1 = 'L2_EFFECT_PARAM1'
    L2_EFFECT_PARAM2 = 'L2_EFFECT_PARAM2'
    L2_EFFECT_PARAM3 = 'L2_EFFECT_PARAM3'
    L2_EFFECT_PARAM4 = 'L2_EFFECT_PARAM4'
    L2_EFFECT_PARAM5 = 'L2_EFFECT_PARAM5'
    L2_EFFECT_PARAM6 = 'L2_EFFECT_PARAM6'
    L2_EFFECT_PARAM7 = 'L2_EFFECT_PARAM7'
    R2_EFFECT_MODE = 'R2_EFFECT_MODE'
    R2_EFFECT_PARAM1 = 'R2_EFFECT_PARAM1'
    R2_EFFECT_PARAM2 = 'R2_EFFECT_PARAM2'
    R2_EFFECT_PARAM3 = 'R2_EFFECT_PARAM3'
    R2_EFFECT_PARAM4 = 'R2_EFFECT_PARAM4'
    R2_EFFECT_PARAM5 = 'R2_EFFECT_PARAM5'
    R2_EFFECT_PARAM6 = 'R2_EFFECT_PARAM6'
    R2_EFFECT_PARAM7 = 'R2_EFFECT_PARAM7'

    LIGHTBAR = 'LIGHTBAR'
    MICROPHONE_LED = 'MICROPHONE_LED'
    MICROPHONE_MUTE = 'MICROPHONE_MUTE'
    LED_OPTIONS = 'LED_OPTIONS'
    PULSE_OPTIONS = 'PULSE_OPTIONS'
    BRIGHTNESS = 'BRIGHTNESS'
    PLAYER_LED = 'PLAYER_LED'


StateValueType = TypeVar('StateValueType')
MappedStateValueType = TypeVar('MappedStateValueType')
StateNameEnumType = TypeVar('StateNameEnumType')
_StChCb0 = Callable[[], None]
_StChCb1 = Callable[[Any], None]
_StChCb2 = Callable[[Any, int | None], None]
_StChCb3 = Callable[[Any, Any, int | None], None]
_StChCb4 = Callable[[ReadStateName, Any, Any, int | None], None]
StateChangeCb = _StChCb0 | _StChCb1 | _StChCb2 | _StChCb3 | _StChCb4

CompareResult = tuple[bool, StateValueType]
CompareFn = Callable[[StateValueType, StateValueType, ...], CompareResult]
Number = int | float
MapFn = Callable[[Any], Any]
DetermineStateValueFn = Callable[[StateValueType, int], StateValueType]

_DEFAULT_NUMBER: Final[Number] = -99999
_HALF_255: Final[Number] = 127.5


@dataclass(frozen=True, slots=True)
class Connection:
    connected: bool = False
    connection_type: ConnectionType = None


@dataclass(frozen=True, slots=True)
class JoyStick:
    x: int = _DEFAULT_NUMBER
    y: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Gyroscope:
    x: int = _DEFAULT_NUMBER
    y: int = _DEFAULT_NUMBER
    z: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Accelerometer:
    x: int = _DEFAULT_NUMBER
    y: int = _DEFAULT_NUMBER
    z: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class TouchFinger:
    active: bool = False
    id: int = _DEFAULT_NUMBER
    x: int = _DEFAULT_NUMBER
    y: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Battery:
    level_percentage: float = _DEFAULT_NUMBER
    full: bool = False
    charging: bool = False


@dataclass(frozen=True, slots=True)
class Feedback:
    active: bool = False
    value: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Orientation:
    pitch: float = _DEFAULT_NUMBER
    roll: float = _DEFAULT_NUMBER
    yaw: float | None = None


def compare(before: StateValueType | None, after: StateValueType) -> CompareResult:
    return (True, after) if before != after else (False, after)


def compare_joystick(
        before: JoyStick | None,
        after: JoyStick,
        deadzone: Number = 0,
) -> CompareResult:
    if before is None:
        return True, after
    if deadzone > 0 and (((after.x - _HALF_255) ** 2) + ((after.y - _HALF_255) ** 2)) <= (deadzone ** 2):
        after = JoyStick(_HALF_255, _HALF_255)

    changed: bool = after.x != before.x or after.y != before.y
    return changed, after


def compare_shoulder_key(
        before: int | None,
        after: int,
        deadzone: Number = 0,
) -> CompareResult:
    if before is None:
        return True, after
    if deadzone > 0 and after <= deadzone:
        after = 0
    changed: bool = after != before
    return changed, after


# TODO: refact that compare fcts
def compare_gyroscope(
        before: Gyroscope,
        after: Gyroscope,
        threshold: Number = 0
) -> CompareResult:
    if before is None:
        return True, after
    if threshold > 0:
        if abs(after.x - before.x) < threshold \
                and abs(after.y - before.y) < threshold \
                and abs(after.z - before.z) < threshold:
            after = Gyroscope(before.x, before.y, before.z)
    changed: bool = after.x != before.x or after.y != before.y or after.z != before.z
    return changed, after


def compare_accelerometer(
        before: Accelerometer,
        after: Accelerometer,
        threshold: Number = 0
) -> CompareResult:
    if before is None:
        return True, after
    if threshold > 0:
        if abs(after.x - before.x) < threshold \
                and abs(after.y - before.y) < threshold \
                and abs(after.z - before.z) < threshold:
            after = Gyroscope(before.x, before.y, before.z)
    changed: bool = after.x != before.x or after.y != before.y or after.z != before.z
    return changed, after


def compare_touch_finger(
        before: TouchFinger,
        after: TouchFinger
) -> CompareResult:
    if before is None:
        return True, after
    changed: bool = after.active != before.active or after.x != before.x or after.y != before.y or after.id != before.id
    return changed, after


def compare_battery(
        before: Battery,
        after: Battery
) -> CompareResult:
    if before is None:
        return True, after
    changed: bool = (
            after.level_percentage != before.level_percentage
            or after.full != before.full
            or after.charging != before.charging
    )
    return changed, after


def compare_feedback(
        before: Feedback,
        after: Feedback
) -> CompareResult:
    if before is None:
        return True, after
    changed: bool = after.active != before.active or after.value != before.value
    return changed, after


def compare_orientation(
        before: Orientation,
        after: Orientation,
        threshold: Number = 0
) -> CompareResult:
    if before is None:
        return True, after
    if threshold > 0:
        if abs(after.yaw - before.yaw) < threshold \
                and abs(after.pitch - before.pitch) < threshold \
                and abs(after.roll - before.roll) < threshold:
            after = Orientation(before.yaw, before.pitch, before.roll)
    changed: bool = after.yaw != before.yaw or after.pitch != before.pitch or after.roll != before.roll
    return changed, after


# ######### MAPPING #######

FromToTuple = tuple[Number, Number, Number, Number]


@dataclass(frozen=True, slots=True)
class Integer:
    value_type: type[Number] = int


@dataclass(frozen=True, slots=True)
class Float:
    value_type: type[Number] = float
    round_digits: int = 2


NumberType = Integer | Float


@dataclass(frozen=True, slots=True)
class FromTo:
    from_min: int
    from_max: int
    to_min: Number
    to_max: Number
    from_type: NumberType = Integer()
    to_type: NumberType = Integer()

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

    left_shoulder_key: FromTo = None
    left_shoulder_key_deadzone: FromTo = None

    right_shoulder_key: FromTo = None
    right_shoulder_key_deadzone: FromTo = None

    set_motor_left: FromTo = None
    set_motor_right: FromTo = None


#
# omitted maps will be handled as raw values
#

class StateValueMapping(Enum):
    # # no need to fill StateValueMapping.RAW, only for illustration
    # # stick y-axis: 0 ... 255, shoulder key: 0 ... 255
    # RAW = StateValueMappingData(
    #     left_stick_x=FromTo(0, 255, 0, 255),
    #     left_stick_y=FromTo(0, 255, 0, 255),
    #     left_stick_deadzone=FromTo(0, 255, 0, 255),
    #     right_stick_x=FromTo(0, 255, 0, 255),
    #     right_stick_y=FromTo(0, 255, 0, 255),
    #     right_stick_deadzone=FromTo(0, 255, 0, 255),
    #     left_shoulder_key=FromTo(0, 255, 0, 255),
    #     left_shoulder_key_deadzone=FromTo(0, 255, 0, 255),
    #     right_shoulder_key=FromTo(0, 255, 0, 255),
    #     right_shoulder_key_deadzone=FromTo(0, 255, 0, 255),
    #     set_motor_left=FromTo(0, 255, 0, 255),
    #     set_motor_right=FromTo(0, 255, 0, 255),
    # ),
    # # thats why
    RAW = None

    # stick y-axis: -100 ... 100, shoulder key: 0 ... 100
    HUNDRED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -100, 100),
        left_stick_y=FromTo(0, 255, 100, -100),
        left_stick_deadzone=FromTo(0, 255, 0, 100),
        right_stick_x=FromTo(0, 255, -100, 100),
        right_stick_y=FromTo(0, 255, 100, -100),
        right_stick_deadzone=FromTo(0, 255, 0, 100),
        left_shoulder_key=FromTo(0, 255, 0, 100),
        left_shoulder_key_deadzone=FromTo(0, 255, 0, 100),
        right_shoulder_key=FromTo(0, 255, 0, 100),
        right_shoulder_key_deadzone=FromTo(0, 255, 0, 100),
        set_motor_left=FromTo(0, 255, 0, 100),
        set_motor_right=FromTo(0, 255, 0, 100),
    )

    # stick y-axis: 255 ... 0, shoulder key: 0 ... 255
    RAW_INVERTED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, 0, 255),
        left_stick_y=FromTo(0, 255, 255, 0),
        right_stick_x=FromTo(0, 255, 0, 255),
        right_stick_y=FromTo(0, 255, 255, 0),
        # undefined maps handled like StateValueMapping.RAW
    )

    DEFAULT = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -128, 127),
        left_stick_y=FromTo(0, 255, 127, -128),
        right_stick_x=FromTo(0, 255, -128, 127),
        right_stick_y=FromTo(0, 255, 127, -128),
        # undefined maps handled like StateValueMapping.RAW
    )

    DEFAULT_INVERTED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -128, 127),
        left_stick_y=FromTo(0, 255, -128, 127),
        right_stick_x=FromTo(0, 255, -128, 127),
        right_stick_y=FromTo(0, 255, -128, 127),
        # undefined maps handled like StateValueMapping.RAW
    )

    NORMALIZED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        left_stick_y=FromTo(0, 255, 1.0, -1.0, to_type=Float()),
        left_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        right_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        right_stick_y=FromTo(0, 255, 1.0, -1.0, to_type=Float()),
        right_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        left_shoulder_key=FromTo(0, 255, 0, 1.0, to_type=Float()),
        left_shoulder_key_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_shoulder_key=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_shoulder_key_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_left=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_right=FromTo(0, 255, 0, 1.0, to_type=Float()),
    )

    NORMALIZED_INVERTED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        left_stick_y=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        left_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        right_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        right_stick_y=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        right_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        left_shoulder_key=FromTo(0, 255, 0, 1.0, to_type=Float()),
        left_shoulder_key_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_shoulder_key=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_shoulder_key_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_left=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_right=FromTo(0, 255, 0, 1.0, to_type=Float()),
    )
