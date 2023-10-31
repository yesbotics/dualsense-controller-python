from __future__ import annotations

from enum import Enum


class WriteStateName(str, Enum):
    FLAGS_CONTROLS = 'FLAGS_CONTROLS'
    FLAGS_PHYSICS = 'FLAGS_PHYSICS'

    MOTOR_LEFT = 'MOTOR_LEFT'
    MOTOR_RIGHT = 'MOTOR_RIGHT'

    LEFT_TRIGGER_EFFECT = 'LEFT_TRIGGER_EFFECT'
    LEFT_TRIGGER_EFFECT_MODE = 'LEFT_TRIGGER_EFFECT_MODE'
    LEFT_TRIGGER_EFFECT_PARAM1 = 'LEFT_TRIGGER_EFFECT_PARAM1'
    LEFT_TRIGGER_EFFECT_PARAM2 = 'LEFT_TRIGGER_EFFECT_PARAM2'
    LEFT_TRIGGER_EFFECT_PARAM3 = 'LEFT_TRIGGER_EFFECT_PARAM3'
    LEFT_TRIGGER_EFFECT_PARAM4 = 'LEFT_TRIGGER_EFFECT_PARAM4'
    LEFT_TRIGGER_EFFECT_PARAM5 = 'LEFT_TRIGGER_EFFECT_PARAM5'
    LEFT_TRIGGER_EFFECT_PARAM6 = 'LEFT_TRIGGER_EFFECT_PARAM6'
    LEFT_TRIGGER_EFFECT_PARAM7 = 'LEFT_TRIGGER_EFFECT_PARAM7'

    RIGHT_TRIGGER_EFFECT = 'RIGHT_TRIGGER_EFFECT'
    RIGHT_TRIGGER_EFFECT_MODE = 'RIGHT_TRIGGER_EFFECT_MODE'
    RIGHT_TRIGGER_EFFECT_PARAM1 = 'RIGHT_TRIGGER_EFFECT_PARAM1'
    RIGHT_TRIGGER_EFFECT_PARAM2 = 'RIGHT_TRIGGER_EFFECT_PARAM2'
    RIGHT_TRIGGER_EFFECT_PARAM3 = 'RIGHT_TRIGGER_EFFECT_PARAM3'
    RIGHT_TRIGGER_EFFECT_PARAM4 = 'RIGHT_TRIGGER_EFFECT_PARAM4'
    RIGHT_TRIGGER_EFFECT_PARAM5 = 'RIGHT_TRIGGER_EFFECT_PARAM5'
    RIGHT_TRIGGER_EFFECT_PARAM6 = 'RIGHT_TRIGGER_EFFECT_PARAM6'
    RIGHT_TRIGGER_EFFECT_PARAM7 = 'RIGHT_TRIGGER_EFFECT_PARAM7'

    LIGHTBAR = 'LIGHTBAR'
    LIGHTBAR_RED = 'LIGHTBAR_RED'
    LIGHTBAR_GREEN = 'LIGHTBAR_GREEN'
    LIGHTBAR_BLUE = 'LIGHTBAR_BLUE'
    LIGHTBAR_ON_OFF = 'LIGHTBAR_ON_OFF'
    LIGHTBAR_PULSE_OPTIONS = 'LIGHTBAR_PULSE_OPTIONS'

    LED_OPTIONS = 'LED_OPTIONS'

    PLAYER_LEDS = "PLAYER_LEDS"
    PLAYER_LEDS_BRIGHTNESS = 'PLAYER_LEDS_BRIGHTNESS'
    PLAYER_LEDS_ENABLE = 'PLAYER_LEDS_ENABLE'

    MICROPHONE = "MICROPHONE"
    MICROPHONE_LED = 'MICROPHONE_LED'
    MICROPHONE_MUTE = 'MICROPHONE_MUTE'


#
# Not clear

# #### pydualsense says:
# flags determing what changes this packet will perform
# 0x01 set the main motors (also requires flag 0x02); setting this by itself will allow rumble to gracefully terminate and then re-enable audio haptics, whereas not setting it will kill the rumble instantly and re-enable audio haptics.
# 0x02 set the main motors (also requires flag 0x01; without bit 0x01 motors are allowed to time out without re-enabling audio haptics)
# 0x04 set the right trigger motor
# 0x08 set the left trigger motor
# 0x10 modification of audio volume
# 0x20 toggling of internal speaker while headset is connected
# 0x40 modification of microphone volume
# #### ds5ctl says:


class OperatingMode(int, Enum):
    DS4_COMPATIBILITY_MODE = 1 << 0
    DS5_MODE = 1 << 1


class FlagsPhysics(int, Enum):
    ENABLE_HAPTICS = 1 << 0 | 1 << 1
    TRIGGER_EFFECTS_RIGHT = 1 << 2
    TRIGGER_EFFECTS_LEFT = 1 << 3
    ALL = 0xff


class FlagsControls(int, Enum):
    MIC_MUTE_LED_CONTROL_ENABLE = 1 << 0
    POWER_SAVE_CONTROL_ENABLE = 1 << 1
    LIGHTBAR_CONTROL_ENABLE = 1 << 2
    RELEASE_LEDS = 1 << 3
    PLAYER_INDICATOR_CONTROL_ENABLE = 1 << 4
    UNKNOWN_FLAG_5 = 1 << 5
    OVERALL_EFFECT_POWER = 1 << 6
    UNKNOWN_FLAG_7 = 1 << 7
    ALL = (
        # RELEASE_LEDS |
            MIC_MUTE_LED_CONTROL_ENABLE |
            POWER_SAVE_CONTROL_ENABLE |
            LIGHTBAR_CONTROL_ENABLE |
            PLAYER_INDICATOR_CONTROL_ENABLE |
            OVERALL_EFFECT_POWER
    )
    ALL_BUT_MUTE_LED = (
        # RELEASE_LEDS |
        # MIC_MUTE_LED_CONTROL_ENABLE |
            POWER_SAVE_CONTROL_ENABLE |
            LIGHTBAR_CONTROL_ENABLE |
            PLAYER_INDICATOR_CONTROL_ENABLE |
            OVERALL_EFFECT_POWER
    )
    ALL_FORCE = 0xff


class PlayerLedsEnable(int, Enum):
    OFF = 0
    # Enables the single, center LED
    CENTER = 0b00100
    # Enables the two LEDs adjacent to and directly surrounding the CENTER LED
    INNER = 0b01010
    # Enables the two outermost LEDs surrounding the INNER LEDs
    OUTER = 0b10001
    ALL = CENTER | INNER | OUTER


class PlayerLedsBrightness(int, Enum):
    HIGH = 0
    MEDIUM = 0x01
    LOW = 0x02


class LightbarMode(int, Enum):
    LIGHT_ON = 1 << 0
    LIGHT_OFF = 1 << 1


class LightbarPulseOptions(int, Enum):
    OFF = 0
    FADE_IN_BLUE = 1 << 0
    FADE_OUT_BLUE = 1 << 1


class LedOptions(int, Enum):
    OFF = 0
    PLAYER_LED_BRIGHTNESS = 1 << 0
    UNINTERRUMPABLE_LED = 1 << 1
    ALL = PLAYER_LED_BRIGHTNESS | UNINTERRUMPABLE_LED


class TriggerEffectMode(int, Enum):
    NO_RESISTANCE = 0x00
    CONTINUOUS_RESISTANCE = 0x01
    SECTION_RESISTANCE = 0x02
    VIBRATING = 0x06
    EFFECT_EXTENDED = 0x26  # Used also for automatic gun
    CALIBRATE = 0xFC
    # new
    BOW = 0x22
    SEMI_AUTOMATIC_GUN = 0x25
    GALLOPING = 0x23
