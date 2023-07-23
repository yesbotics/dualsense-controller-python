from enum import Enum
from typing import Final, TypeVar, Callable, Any

VENDOR_ID: Final[int] = 0x054c
PRODUCT_ID: Final[int] = 0x0ce6
OUTPUT_REPORT_USB: Final[int] = 0x02
OUTPUT_REPORT_BT: Final[int] = 0x31

CONNECTION_LOOKUP_INTERVAL: Final[int] = 1  # one second


class InReportLength(int, Enum):
    DUMMY = 100
    USB_01 = 64
    BT_31 = 78
    BT_01 = 10


class OutReportLength(int, Enum):
    USB_01 = InReportLength.USB_01
    BT_31 = InReportLength.BT_31
    BT_01 = InReportLength.BT_01
    # USB_01 = 47
    # BT_31 = 77
    # BT_01 = 77  # ??


#
# Not clear
#
class OutOperatingMode(int, Enum):
    # Alternativ:
    # DS4_COMPATIBILITY_MODE = 1 << 0
    # DS5_MODE = 1 << 1
    COMPATIBLE_VIBRATION = 1 << 0
    HAPTICS_SELECT = 1 << 1
    ALL = (
            COMPATIBLE_VIBRATION |
            HAPTICS_SELECT
    )


class OutLightEffectControl(int, Enum):
    MIC_MUTE_LED_CONTROL_ENABLE = 1 << 0
    POWER_SAVE_CONTROL_ENABLE = 1 << 1
    LIGHTBAR_CONTROL_ENABLE = 1 << 2
    RELEASE_LEDS = 1 << 3
    PLAYER_INDICATOR_CONTROL_ENABLE = 1 << 4
    UNKNOWN_FLAG_5 = 1 << 5
    OVERALL_EFFECT_POWER = 1 << 6
    UNKNOWN_FLAG_7 = 1 << 7
    ALL = (
            MIC_MUTE_LED_CONTROL_ENABLE |
            POWER_SAVE_CONTROL_ENABLE |
            LIGHTBAR_CONTROL_ENABLE |
            RELEASE_LEDS |
            PLAYER_INDICATOR_CONTROL_ENABLE |
            OVERALL_EFFECT_POWER
    )
    ALL_FORCE = 0xff


class OutPlayerLed(int, Enum):
    PLAYER_1 = 1 << 0
    PLAYER_2 = 1 << 1
    PLAYER_3 = 1 << 2
    PLAYER_4 = 1 << 3
    ALL = PLAYER_1 | PLAYER_2 | PLAYER_3 | PLAYER_4
    # PLAYER_1 = 4
    # PLAYER_2 = 10
    # PLAYER_3 = 21
    # PLAYER_4 = 27
    # ALL = 31


class OutBrightness(int, Enum):
    HIGH = 0
    MEDIUM = 1 << 0
    LOW = 1 << 1


class OutPulseOptions(int, Enum):
    OFF = 0
    FADE_BLUE = 1 << 0
    FADE_OUT = 1 << 1


class OutLedOptions(int, Enum):
    OFF = 0
    PLAYER_LED_BRIGHTNESS = 1 << 0
    UNINTERRUMPABLE_LED = 1 << 1
    ALL = (
            PLAYER_LED_BRIGHTNESS |
            UNINTERRUMPABLE_LED
    )


class OutReportId(int, Enum):
    USB_01 = 0x02
    BT_31 = 0x31
    BT_01 = 0x31  # ??


class ConnectionType(Enum):
    UNDEFINED = 'UNDEFINED',
    USB_01 = 'USB',
    BT_31 = 'BT',
    BT_01 = 'BT'


class WriteStateName(str, Enum):
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


class EventType(str, Enum):
    EXCEPTION = 'EXCEPTION'
    CONNECTION_CHANGE = 'CONNECTION_CHANGE',


def flag(bit: int) -> int:
    return 1 << bit


ValueType = TypeVar('ValueType')

ExceptionCallback = Callable[[Exception], None]
SimpleCallback = Callable[[], None]
ConnectionChangeCallback = Callable[[bool, ConnectionType], None]
StateChangeCallback = Callable[[Any, Any], None]
AnyStateChangeCallback = Callable[[ReadStateName, Any, Any], None]
