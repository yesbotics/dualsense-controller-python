from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Microphone:
    mute: bool = True
    led: bool = True
