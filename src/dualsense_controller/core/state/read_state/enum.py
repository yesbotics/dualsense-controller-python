from enum import Enum


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

    LEFT_STICK = 'LEFT_STICK'
    LEFT_STICK_X = 'LEFT_STICK_X'
    LEFT_STICK_Y = 'LEFT_STICK_Y'

    RIGHT_STICK = 'RIGHT_STICK'
    RIGHT_STICK_X = 'RIGHT_STICK_X'
    RIGHT_STICK_Y = 'RIGHT_STICK_Y'

    GYROSCOPE = 'GYROSCOPE'
    GYROSCOPE_X = "GYROSCOPE_X"
    GYROSCOPE_Y = "GYROSCOPE_Y"
    GYROSCOPE_Z = "GYROSCOPE_Z"

    ACCELEROMETER = 'ACCELEROMETER'
    ACCELEROMETER_X = "ACCELEROMETER_X"
    ACCELEROMETER_Y = "ACCELEROMETER_Y"
    ACCELEROMETER_Z = "ACCELEROMETER_Z"

    ORIENTATION = 'ORIENTATION'

    TOUCH_FINGER_1 = 'TOUCH_FINGER_1'
    TOUCH_FINGER_1_ACTIVE = 'TOUCH_FINGER_1_ACTIVE'
    TOUCH_FINGER_1_ID = 'TOUCH_FINGER_1_ID'
    TOUCH_FINGER_1_X = 'TOUCH_FINGER_1_X'
    TOUCH_FINGER_1_Y = 'TOUCH_FINGER_1_Y'
    TOUCH_FINGER_2 = 'TOUCH_FINGER_2'
    TOUCH_FINGER_2_ACTIVE = 'TOUCH_FINGER_2_ACTIVE'
    TOUCH_FINGER_2_ID = 'TOUCH_FINGER_2_ID'
    TOUCH_FINGER_2_X = 'TOUCH_FINGER_2_X'
    TOUCH_FINGER_2_Y = 'TOUCH_FINGER_2_Y'

    LEFT_TRIGGER = "LEFT_TRIGGER"
    LEFT_TRIGGER_VALUE = 'LEFT_TRIGGER_VALUE'
    LEFT_TRIGGER_FEEDBACK = "LEFT_TRIGGER_FEEDBACK"
    LEFT_TRIGGER_FEEDBACK_ACTIVE = 'LEFT_TRIGGER_FEEDBACK_ACTIVE'
    LEFT_TRIGGER_FEEDBACK_VALUE = 'LEFT_TRIGGER_FEEDBACK_VALUE'

    RIGHT_TRIGGER = "RIGHT_TRIGGER"
    RIGHT_TRIGGER_VALUE = 'RIGHT_TRIGGER_VALUE'
    RIGHT_TRIGGER_FEEDBACK = "RIGHT_TRIGGER_FEEDBACK"
    RIGHT_TRIGGER_FEEDBACK_ACTIVE = 'RIGHT_TRIGGER_FEEDBACK_ACTIVE'
    RIGHT_TRIGGER_FEEDBACK_VALUE = 'RIGHT_TRIGGER_FEEDBACK_VALUE'

    BATTERY = "BATTERY"
    BATTERY_LEVEL_PERCENT = 'BATTERY_LEVEL_PERCENT'
    BATTERY_FULL = 'BATTERY_FULL'
    BATTERY_CHARGING = 'BATTERY_CHARGING'
