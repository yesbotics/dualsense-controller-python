from abc import ABC, abstractmethod
from dataclasses import dataclass

from dualsense_controller.core.state.write_state.enum import OutFlagsPhysics, ControlFlags, LedOptions, \
    LightbarPulseOptions, PlayerLedsBrightness, PlayerLedsEnable


@dataclass(slots=True)
class OutReport(ABC):

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    flags_physics: int = OutFlagsPhysics.ALL
    flags_controls: int = ControlFlags.ALL

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

    lightbar_on_off: bool = True

    microphone_led: bool = False
    microphone_mute: bool = True

    led_options: LedOptions = LedOptions.ALL
    lightbar_pulse_options: LightbarPulseOptions = LightbarPulseOptions.OFF
    player_leds_brightness: PlayerLedsBrightness = PlayerLedsBrightness.HIGH
    player_leds_enable: int = PlayerLedsEnable.OFF
