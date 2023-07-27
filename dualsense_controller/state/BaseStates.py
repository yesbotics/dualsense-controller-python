from typing import Final, Generic

from dualsense_controller.state import CompareFn, State, StateNameEnumType, StateValueType


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
            ignore_initial_none: bool = True,
            compare_fn: CompareFn[StateValueType] = None,
            trigger_change_async: bool = False,
            enforce_update: bool = False,
            **kwargs
    ) -> State[StateValueType]:

        if compare_fn is not None:
            compare_fn = BaseStates._wrap_compare_fn(compare_fn, **kwargs)
        state: State[StateValueType] = State[StateValueType](
            name,
            value=value,
            compare_fn=compare_fn,
            enforce_update=enforce_update,
            ignore_initial_none=ignore_initial_none,
            trigger_change_async=trigger_change_async,
        )
        self._states_dict[name] = state
        return state

    @staticmethod
    def _wrap_compare_fn(compare_fn, **kwargs) -> CompareFn:
        def _inner(before, after) -> bool:
            return compare_fn(before, after, **kwargs)

        return _inner
