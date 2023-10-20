from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from dualsense_controller.core.state.typedef import Number
from dualsense_controller.core.state.write_state.enum import LightbarPulseOptions, PlayerLedsEnable, \
    PlayerLedsBrightness, TriggerEffectMode


@dataclass(frozen=True, slots=True)
class Microphone:
    mute: bool = True
    led: bool = True


@dataclass(frozen=True, slots=True)
class Lightbar:
    red: int = 0
    green: int = 0
    blue: int = 0
    is_on: bool = False
    pulse_options: int = LightbarPulseOptions.FADE_OUT_BLUE


@dataclass(frozen=True, slots=True)
class PlayerLeds:
    enable: PlayerLedsEnable = PlayerLedsEnable.OFF
    brightness: PlayerLedsBrightness = PlayerLedsBrightness.MEDIUM


@dataclass(frozen=True, slots=True)
class TriggerEffect:
    mode: int | TriggerEffectMode = TriggerEffectMode.NO_RESISTANCE
    param1: int = 0x00
    param2: int = 0x00
    param3: int = 0x00
    param4: int = 0x00
    param5: int = 0x00
    param6: int = 0x00
    param7: int = 0x00
