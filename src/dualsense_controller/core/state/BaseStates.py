from typing import Final

from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.typedef import StateChangeCallback, StateName, StateValue


class BaseStates:

    def __init__(self, state_value_mapper: StateValueMapper):
        self._states_dict: Final[dict[StateName, State]] = {}
        self._state_value_mapper: Final[StateValueMapper] = state_value_mapper

    @property
    def has_changed_states(self) -> bool:
        return any(True for key, state in self._states_dict.items() if state.has_changed_since_last_set_value)

    def once_change(
            self, name_or_callback: StateName | StateChangeCallback, callback: StateChangeCallback | None = None
    ):
        if callback is None:
            self.once_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).once_change(callback)

    def on_change(
            self, name_or_callback: StateName | StateChangeCallback, callback: StateChangeCallback | None = None
    ):
        if callback is None:
            self.on_any_change(name_or_callback)
        else:
            self._get_state_by_name(name_or_callback).on_change(callback)

    def on_any_change(self, callback: StateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.on_change(callback)

    def once_any_change(self, callback: StateChangeCallback):
        for state_name, state in self._states_dict.items():
            state.once_change(callback)

    def remove_change_listener(
            self, name_or_callback: StateName | StateChangeCallback, callback: StateChangeCallback | None = None
    ) -> None:
        if isinstance(name_or_callback, StateName):
            self._get_state_by_name(name_or_callback).remove_change_listener(callback)
        elif callable(name_or_callback):
            self.remove_any_change_listener(name_or_callback)
        else:
            self.remove_all_change_listeners()

    def remove_all_change_listeners(self) -> None:
        for state_name, state in self._states_dict.items():
            state.remove_all_change_listeners()

    def remove_any_change_listener(self, callback: StateChangeCallback) -> None:
        for state_name, state in self._states_dict.items():
            state.remove_change_listener(callback)

    def _register_state(self, name: StateName, state: State[StateValue]) -> None:
        self._states_dict[name] = state

    def _get_state_by_name(self, name: StateName) -> State[StateValue]:
        return self._states_dict[name]
