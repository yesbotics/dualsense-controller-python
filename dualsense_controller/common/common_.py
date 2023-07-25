from enum import Enum


#
# Not clear
#
class OutFlagsPhysics(int, Enum):
    # Alternativ:
    # DS4_COMPATIBILITY_MODE = 1 << 0
    # DS5_MODE = 1 << 1
    COMPATIBLE_VIBRATION = 1 << 0
    HAPTICS_SELECT = 1 << 1
    ALL = (
            COMPATIBLE_VIBRATION |
            HAPTICS_SELECT
    )


class OutFlagsLights(int, Enum):
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


class OutPlayerLed(int, Enum):
    OFF = 0

    # Enables the single, center LED
    CENTER = 0b00100

    # Enables the two LEDs adjacent to and directly surrounding the CENTER LED
    INNER = 0b01010

    # Enables the two outermost LEDs surrounding the INNER LEDs
    OUTER = 0b10001

    ALL = CENTER | INNER | OUTER


class OutLightbarMode(int, Enum):
    LIGHT_ON = 1 << 0
    LIGHT_OUT = 1 << 1


class OutBrightness(int, Enum):
    HIGH = 0
    MEDIUM = 0x01
    LOW = 0x02


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
