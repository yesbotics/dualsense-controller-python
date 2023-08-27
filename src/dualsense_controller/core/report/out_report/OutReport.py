from abc import ABC, abstractmethod
from dataclasses import dataclass

from dualsense_controller.core.state.write_state.enum import FlagsPhysics, FlagsControls, LedOptions, \
    LightbarPulseOptions, OperatingMode, PlayerLedsBrightness, PlayerLedsEnable


@dataclass(slots=True)
class OutReport(ABC):

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    operating_mode: int = OperatingMode.DS5_MODE
    flags_physics: int = FlagsPhysics.ALL
    flags_controls: int = FlagsControls.ALL

    lightbar_red: int = 0xff
    lightbar_green: int = 0xff
    lightbar_blue: int = 0xff

    motor_left: int = 0x00
    motor_right: int = 0x00

    left_trigger_effect_mode: int = 0x26
    left_trigger_effect_param1: int = 0x90
    left_trigger_effect_param2: int = 0xA0
    left_trigger_effect_param3: int = 0xFF
    left_trigger_effect_param4: int = 0x00
    left_trigger_effect_param5: int = 0x00
    left_trigger_effect_param6: int = 0x00
    left_trigger_effect_param7: int = 0x00

    right_trigger_effect_mode: int = 0x26
    right_trigger_effect_param1: int = 0x90
    right_trigger_effect_param2: int = 0xA0
    right_trigger_effect_param3: int = 0xFF
    right_trigger_effect_param4: int = 0x00
    right_trigger_effect_param5: int = 0x00
    right_trigger_effect_param6: int = 0x00
    right_trigger_effect_param7: int = 0x00

    lightbar_on_off: bool = True

    microphone_led: bool = False
    microphone_mute: bool = True

    led_options: LedOptions = LedOptions.ALL
    lightbar_pulse_options: LightbarPulseOptions = LightbarPulseOptions.OFF
    player_leds_brightness: PlayerLedsBrightness = PlayerLedsBrightness.HIGH
    player_leds_enable: int = PlayerLedsEnable.OFF
