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

    @property
    def value(self) -> PropertyType:
        return self._state.get_value_mapped()


class BoolProperty(Property[bool], ABC):

    def _on_true(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, True))

    def _on_false(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, False))

    @staticmethod
    def _on_changed(callback: PropertyChangeCallback, expected_value: bool, actual_value: bool):
        if expected_value == actual_value:
            callback()


class ButtonProperty(BoolProperty):

    def on_down(self, callback: PropertyChangeCallback):
        self._on_true(callback)

    def on_up(self, callback: PropertyChangeCallback):
        self._on_false(callback)

    @property
    def pressed(self) -> bool:
        return self.value


class TriggerProperty(Property[Number]):
    pass
