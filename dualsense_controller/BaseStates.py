from typing import Generic, Final

from dualsense_controller import State
from dualsense_controller.common import StateValueType, StateNameEnumType


class BaseStates(Generic[StateNameEnumType]):

    def __init__(self):
        self._states_dict: Final[dict[StateNameEnumType, State]] = {}

    def set_value(self, name: StateNameEnumType, value: StateValueType, trigger_change: bool = True) -> None:
        state: State[StateValueType] = self._get_state_by_name(name)
        if not trigger_change:
            state.set_value_without_triggering_change(value)
        else:
            state.value = value

    def _get_state_by_name(self, name: StateNameEnumType) -> State:
        return self._states_dict[name]

    def _create_and_register_state(
            self,
            name: StateNameEnumType,
            value: StateValueType = None,
            threshold: int = 0,
            skip_none: False = True,
    ) -> State[StateValueType]:
        state: State[StateValueType] = State[StateValueType](
            name,
            value=value,
            threshold=threshold,
            skip_none=skip_none
        )
        self._states_dict[name] = state
        return state
