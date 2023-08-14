from __future__ import annotations

from dataclasses import dataclass

from dualsense_controller.core.report.out_report.enum import LightbarPulseOptions, PlayerLedsBrightness, \
    PlayerLedsEnable


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
