from __future__ import annotations

from dataclasses import dataclass


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
