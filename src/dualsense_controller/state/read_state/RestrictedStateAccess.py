from typing import Callable, Generic

from dualsense_controller.state.State import State
from dualsense_controller.state.typedef import StateChangeCallback, StateValueType


class RestrictedStateAccess(Generic[StateValueType]):
    def __init__(self, state: State[StateValueType]):
        self._state = state

    @property
    def value(self) -> StateValueType | None:
        return self._state.get_value_mapped()

    @property
    def changed(self) -> bool:
        return self._state.has_changed

    @property
    def last_value(self) -> StateValueType | None:
        return self._state.get_last_value_mapped()

    @property
    def on_change(self) -> Callable[[StateChangeCallback], None]:
        return self._state.on_change

    @property
    def remove_change_listener(self) -> Callable[[StateChangeCallback | None], None]:
        return self._state.remove_change_listener

    @property
    def remove_all_change_listeners(self) -> Callable[[], None]:
        return self._state.remove_all_change_listeners
