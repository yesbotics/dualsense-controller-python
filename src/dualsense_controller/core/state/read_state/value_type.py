from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.state.typedef import Number

_DEFAULT_NUMBER: Final[Number] = -99999


@dataclass(frozen=True, slots=True)
class Connection:
    connected: bool = False
    connection_type: ConnectionType = None


@dataclass(frozen=True, slots=True)
class JoyStick:
    x: Number = _DEFAULT_NUMBER
    y: Number = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Gyroscope:
    x: int = _DEFAULT_NUMBER
    y: int = _DEFAULT_NUMBER
    z: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Accelerometer:
    x: int = _DEFAULT_NUMBER
    y: int = _DEFAULT_NUMBER
    z: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class TouchFinger:
    active: bool = False
    id: int = _DEFAULT_NUMBER
    x: int = _DEFAULT_NUMBER
    y: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Battery:
    level_percentage: float = _DEFAULT_NUMBER
    full: bool = False
    charging: bool = False


@dataclass(frozen=True, slots=True)
class TriggerFeedback:
    active: bool = False
    value: int = _DEFAULT_NUMBER


@dataclass(frozen=True, slots=True)
class Trigger:
    value: Number = _DEFAULT_NUMBER
    feedback: TriggerFeedback = TriggerFeedback()


@dataclass(frozen=True, slots=True)
class Orientation:
    pitch: float = _DEFAULT_NUMBER
    roll: float = _DEFAULT_NUMBER
    yaw: float | None = None
