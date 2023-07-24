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
        self._last_value: StateValueType | None = None
        self._changed_since_last_update: bool = False
        # extra
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
            self.change_value(old_value=self._value, new_value=value, trigger_change=False)
            return
        if isinstance(value, int):
            if old_value != value:
                if old_value is None or abs(value - old_value) >= self._threshold:
                    self.change_value(old_value=old_value, new_value=value)
                else:
                    self.do_not_change_value()
        else:
            if old_value != value:
                self.change_value(old_value=old_value, new_value=value)
            else:
                self.do_not_change_value()

    @property
    def last_value(self) -> StateValueType:
        return self._last_value

    @property
    def changed(self) -> bool:
        return self._changed_since_last_update

    def set_value_without_triggering_change(self, new_value: StateValueType | None):
        self.change_value(old_value=self._value, new_value=new_value, trigger_change=False)

    def on_change(self, callback: StateChangeCallback) -> None:
        self._event_emitter.on(self.name, callback)

    def change_value(
            self,
            old_value: StateValueType,
            new_value: StateValueType,
            trigger_change: bool = True,
    ) -> None:
        self._last_value = old_value
        self._value = new_value
        self._changed_since_last_update = True
        if trigger_change:
            self._event_emitter.emit(self.name, old_value, new_value)

    def do_not_change_value(self) -> None:
        self._changed_since_last_update = False
