from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .enum import OutFlagsPhysics, OutFlagsLights, OutLedOptions, OutPulseOptions, OutBrightness, OutPlayerLed


@dataclass(slots=True)
class OutReport(ABC):

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    flags_physics: int = OutFlagsPhysics.ALL
    flags_lights: int = OutFlagsLights.ALL

    lightbar_red: int = 0xff
    lightbar_green: int = 0xff
    lightbar_blue: int = 0xff

    motor_left: int = 0x00
    motor_right: int = 0x00

    l2_effect_mode: int = 0x26
    l2_effect_param1: int = 0x90
    l2_effect_param2: int = 0xA0
    l2_effect_param3: int = 0xFF
    l2_effect_param4: int = 0x00
    l2_effect_param5: int = 0x00
    l2_effect_param6: int = 0x00
    l2_effect_param7: int = 0x00

    r2_effect_mode: int = 0x26
    r2_effect_param1: int = 0x90
    r2_effect_param2: int = 0xA0
    r2_effect_param3: int = 0xFF
    r2_effect_param4: int = 0x00
    r2_effect_param5: int = 0x00
    r2_effect_param6: int = 0x00
    r2_effect_param7: int = 0x00

    lightbar: bool = True

    microphone_led: bool = False
    microphone_mute: bool = True

    led_options: OutLedOptions = OutLedOptions.ALL
    pulse_options: OutPulseOptions = OutPulseOptions.OFF
    brightness: OutBrightness = OutBrightness.HIGH
    player_led: int = OutPlayerLed.OFF
