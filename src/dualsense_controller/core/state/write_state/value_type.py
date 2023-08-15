from __future__ import annotations

from dataclasses import dataclass

from dualsense_controller.core.state.typedef import Number
from dualsense_controller.core.state.write_state.enum import LightbarPulseOptions, PlayerLedsEnable, \
    PlayerLedsBrightness


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
    mode: TriggerEffectMode


@dataclass(frozen=True, slots=True)
class Trigger:
    value: Number
    effect: TriggerEffect
