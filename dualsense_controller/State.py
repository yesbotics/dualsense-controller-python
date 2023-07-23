from typing import Generic, Final

import pyee

from dualsense_controller.common import StateValueType, ReadStateName, StateChangeCallback


class State(Generic[StateValueType]):
    def __init__(
            self,
            name: ReadStateName,
            value: StateValueType = None,
            threshold: int = 0,
            skip_none: bool = True,
    ):
        super().__init__()
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()
        self.name: Final[ReadStateName] = name
        self._value: StateValueType | None = value
        self._threshold: int = threshold
        self._skip_none: bool = skip_none

    def __repr__(self) -> str:
        return f'State[{type(self.value).__name__}]({self.name}: {self.value})'

    @property
    def threshold(self) -> int:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int) -> None:
        self._threshold = threshold

    @property
    def value(self) -> StateValueType:
        return self._value

    @value.setter
    def value(self, value: StateValueType | None) -> None:
        old_value: StateValueType = self._value
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

    def set_value_without_triggering_change(self, new_value: StateValueType | None):
        self._value = new_value

    def on_change(self, callback: StateChangeCallback) -> None:
        self._event_emitter.on(self.name, callback)

    def _set_value(self, old_value: StateValueType, new_value: StateValueType) -> None:
        self._value = new_value
        self._event_emitter.emit(self.name, old_value, new_value)
