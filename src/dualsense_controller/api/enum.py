from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class _UpdateLevelData:
    enforce_update: bool
    can_update_itself: bool


class UpdateLevel(Enum):
    # reactive, only update value if requested or has listeners
    LAZY = _UpdateLevelData(
        enforce_update=False,
        can_update_itself=True,
    )
    # proactive, always update all values
    PAINSTAKING = _UpdateLevelData(
        enforce_update=True,
        can_update_itself=False,
    )
    # passive, only update values, which are listened
    HAENGBLIEM = _UpdateLevelData(
        enforce_update=False,
        can_update_itself=False,
    )
    DEFAULT = LAZY
