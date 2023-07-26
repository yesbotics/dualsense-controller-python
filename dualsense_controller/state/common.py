from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, TypeVar


class ReadStateName(str, Enum):
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

    TOUCH_0_ACTIVE = 'TOUCH_0_ACTIVE'
    TOUCH_0_ID = 'TOUCH_0_ID'
    TOUCH_0_X = 'TOUCH_0_X'
    TOUCH_0_Y = 'TOUCH_0_Y'
    TOUCH_1_ACTIVE = 'TOUCH_1_ACTIVE'
    TOUCH_1_ID = 'TOUCH_1_ID'
    TOUCH_1_X = 'TOUCH_1_X'
    TOUCH_1_Y = 'TOUCH_1_Y'

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
StateChangeCallback = Callable[[Any, Any], None]
AnyStateChangeCallback = Callable[[ReadStateName, Any, Any], None]

CompareResult = tuple[bool, StateValueType]
CompareFn = Callable[[StateValueType, StateValueType, ...], CompareResult]
MapFn = Callable[[StateValueType], MappedStateValueType]


@dataclass(frozen=True, slots=True)
class JoyStick:
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class Gyroscope:
    x: int
    y: int
    z: int


@dataclass(frozen=True, slots=True)
class Accelerometer:
    x: int
    y: int
    z: int


@dataclass(frozen=True, slots=True)
class Orientation:
    yaw: int
    pitch: int
    roll: int


def compare(before: StateValueType | None, after: StateValueType) -> CompareResult:
    return (True, after) if before != after else (False, after)


def compare_joystick(before: JoyStick | None, after: JoyStick, deadzone: int = 0) -> CompareResult:
    if before is None:
        return True, after
    if deadzone > 0 and (((after.x - 127) ** 2) + ((after.y - 127) ** 2)) <= deadzone ** 2:
        after = JoyStick(127, 127)
    changed: bool = after.x != before.x or after.y != before.y
    return changed, after


def compare_shoulder_key(before: int | None, after: int, deadzone: int = 0) -> CompareResult:
    if before is None:
        return True, after
    if deadzone > 0 and after <= deadzone:
        after = 0
    changed: bool = after != before
    return changed, after


def compare_gyroscope(before: Gyroscope, after: Gyroscope, threshold: int = 0) -> CompareResult:
    if before is None:
        return True, after
    if threshold > 0:
        if abs(after.x - before.x) < threshold \
                and abs(after.y - before.y) < threshold \
                and abs(after.z - before.z) < threshold:
            after = Gyroscope(before.x, before.y, before.z)
    changed: bool = after.x != before.x or after.y != before.y or after.z != before.z
    return changed, after


def compare_accel(before: Accelerometer, after: Accelerometer, threshold: int = 0) -> CompareResult:
    if before is None:
        return True, after
    if threshold > 0:
        if abs(after.x - before.x) < threshold \
                and abs(after.y - before.y) < threshold \
                and abs(after.z - before.z) < threshold:
            after = Gyroscope(before.x, before.y, before.z)
    changed: bool = after.x != before.x or after.y != before.y or after.z != before.z
    return changed, after


def compare_orientation(before: Orientation, after: Orientation, threshold: int = 0) -> CompareResult:
    if before is None:
        return True, after
    if threshold > 0:
        if abs(after.yaw - before.yaw) < threshold \
                and abs(after.pitch - before.pitch) < threshold \
                and abs(after.roll - before.roll) < threshold:
            after = Orientation(before.yaw, before.pitch, before.roll)
    changed: bool = after.yaw != before.yaw or after.pitch != before.pitch or after.roll != before.roll
    return changed, after


Number = int | float
FromToTuple = tuple[Number, Number, Number, Number]


@dataclass(frozen=True, slots=True)
class StateValueMappingData:
    left_stick_x: FromToTuple = None
    left_stick_y: FromToTuple = None
    right_stick_x: FromToTuple = None
    right_stick_y: FromToTuple = None
    left_shoulder_key: FromToTuple = None
    right_shoulder_key: FromToTuple = None


class StateValueMapping(Enum):
    RAW = StateValueMappingData()
    KAPPA_J = StateValueMappingData(
        left_stick_x=(0, 255, -128, 127),
        left_stick_y=(0, 255, 127, -128),
        right_stick_x=(0, 255, -128, 127),
        right_stick_y=(0, 255, 127, -128),
        left_shoulder_key=(0, 255, 0, 255),
        right_shoulder_key=(0, 255, 0, 255),
    ),
    EINSPUNKTNULL = StateValueMappingData(
        left_stick_x=(0, 255, -128, 127),
        left_stick_y=(0, 255, -128, 127),
        right_stick_x=(0, 255, -128, 127),
        right_stick_y=(0, 255, -128, 127),
        left_shoulder_key=(0, 255, 0, 255),
        right_shoulder_key=(0, 255, 0, 255),
    ),
    FOR_NOOBS = StateValueMappingData(
        left_stick_x=(0, 255, -1.0, 1.0),
        left_stick_y=(0, 255, 1.0, -1.0),
        right_stick_x=(0, 255, -1.0, 1.0),
        right_stick_y=(0, 255, 1.0, -1.0),
        left_shoulder_key=(0, 255, 0, 1.0),
        right_shoulder_key=(0, 255, 0, 1.0),
    ),
    FOR_BOONS = StateValueMappingData(
        left_stick_x=(0, 255, -1.0, 1.0),
        left_stick_y=(0, 255, 1.0, -1.0),
        right_stick_x=(0, 255, 1.0, -1.0),
        right_stick_y=(0, 255, 1.0, -1.0),
        left_shoulder_key=(0, 255, 0, 1.0),
        right_shoulder_key=(0, 255, 0, 1.0),
    ),
