from enum import Enum
from typing import Final, TypeVar, Callable, Any

VENDOR_ID: Final[int] = 0x054c
PRODUCT_ID: Final[int] = 0x0ce6
OUTPUT_REPORT_USB: Final[int] = 0x02
OUTPUT_REPORT_BT: Final[int] = 0x31

CONNECTION_LOOKUP_INTERVAL: Final[int] = 1  # one second


class ReportLength(int, Enum):
    DUMMY = 100
    USB_01 = 64
    BT_31 = 78
    BT_01 = 10


class ConnectionType(Enum):
    UNDEFINED = 'UNDEFINED',
    USB_01 = 'USB',
    BT_31 = 'BT',
    BT_01 = 'BT'


class StateName(str, Enum):
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
    CONNECTION_LOOKUP = 'CONNECTION_LOOKUP',
    CONNECTION_CHANGE = 'CONNECTION_CHANGE',


SimpleCallback = Callable[[], None]
ConnectionChangeCallback = Callable[[bool, ConnectionType], None]
StateChangeCallback = Callable[[Any, Any], None]
AnyStateChangeCallback = Callable[[StateName, Any, Any], None]

ValueType = TypeVar('ValueType')
