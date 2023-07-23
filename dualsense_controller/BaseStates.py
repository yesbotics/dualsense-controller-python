from typing import Generic, TypeVar, Final

from dualsense_controller import State
from dualsense_controller.common import StateValueType, StateNameEnumType


class BaseStates(Generic[StateNameEnumType]):

    def __init__(self):
        self._states_dict: Final[dict[StateNameEnumType, State]] = {}

    def _get_state_by_name(self, name: StateNameEnumType) -> State:
        return self._states_dict[name]

    def _create_and_register_state(
            self,
            name: StateNameEnumType,
            value: StateValueType = None,
            **kwargs
    ) -> State[StateValueType]:
        state: State[StateValueType] = State[StateValueType](name, value, **kwargs)
        self._states_dict[name] = state
        return state
