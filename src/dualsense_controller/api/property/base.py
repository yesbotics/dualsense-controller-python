from abc import ABC
from functools import partial
from typing import Final, Generic

from dualsense_controller.api.typedef import PropertyChangeCallback, PropertyType
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.typedef import Number


class Property(Generic[PropertyType], ABC):

    def __init__(self, state: State[PropertyType]):
        self._state: Final[State[PropertyType]] = state

    def on_change(self, callback: PropertyChangeCallback):
        self._state.on_change(callback)

    def once_change(self, callback: PropertyChangeCallback):
        self._state.once_change(callback)

    @property
    def changed(self) -> bool:
        return self._state.has_changed_since_last_set_value

    def _get_value(self) -> PropertyType:
        return self._state.value

    def _get_last_value(self) -> PropertyType:
        return self._state.last_value

    def _set_value(self, value: Number) -> None:
        self._state.value = value


class GetNumberProperty(Property[Number], ABC):

    @property
    def value(self) -> Number:
        return self._get_value()


class GetSetNumberProperty(Property[Number], ABC):

    @property
    def value(self) -> Number:
        return self._get_value()

    def set(self, value: Number):
        self._set_value(value)


class BoolProperty(Property[bool], ABC):

    def _on_true(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, True))

    def _on_false(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, False))

    @staticmethod
    def _on_changed(callback: PropertyChangeCallback, expected_value: bool, actual_value: bool):
        if expected_value == actual_value:
            callback()
