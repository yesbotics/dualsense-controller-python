from typing import Generic, Final

import pyee

from dualsense_controller import ValueType, StateName


class State(Generic[ValueType], pyee.EventEmitter):
    EVENT_CHANGE: Final[str] = 'change'

    def __init__(
            self,
            name: StateName,
            value: ValueType | None = None,
            skip_none: bool = True,
            threshold: int = 0,
    ):
        super().__init__()
        self.name: Final[StateName] = name
        self._skip_none: bool = skip_none
        self._value: ValueType | None = value
        self._threshold: int = threshold

    @property
    def threshold(self) -> int:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int) -> None:
        self._threshold = threshold

    @property
    def value(self) -> ValueType:
        return self._value

    @value.setter
    def value(self, value: ValueType | None) -> None:
        old_value: ValueType = self._value
        if old_value is None and self._skip_none:
            self._value = value
            return
        if isinstance(value, int):
            if old_value != value:
                if old_value is None or abs(value - old_value) >= self._threshold:
                    self._set_value(old_value, value)
        else:
            if old_value != value:
                self._set_value(old_value, value)

    def _set_value(self, old_value: ValueType, new_value: ValueType) -> None:
        self._value = new_value
        self.emit(State.EVENT_CHANGE, self.name, old_value, new_value)
