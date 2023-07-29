from typing import Any, Final, Generic

from dualsense_controller.state import CompareFn, MapFn, State, StateNameEnumType, StateValueType


class BaseStates(Generic[StateNameEnumType]):

    def __init__(self):
        self._states_dict: Final[dict[StateNameEnumType, State]] = {}

    def set_value(self, name: StateNameEnumType, value: StateValueType, trigger_change: bool = True) -> None:
        state: State[StateValueType] = self._get_state_by_name(name)
        if not trigger_change:
            state.set_value_without_triggering_change(value)
        else:
            state.value = value

    def set_value_mapped(self, name: StateNameEnumType, value: StateValueType, trigger_change: bool = True) -> None:
        print('mappy', name, value, trigger_change)
        state: State[StateValueType] = self._get_state_by_name(name)
        if not trigger_change:
            state.set_value_mapped_without_triggering_change(value)
        else:
            state.value_mapped = value

    def _get_state_by_name(self, name: StateNameEnumType) -> State:
        return self._states_dict[name]

    def _create_and_register_state(
            self,
            name: StateNameEnumType,
            value: StateValueType = None,
            default_value: StateValueType = None,
            ignore_none: bool = True,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn[StateValueType] = None,
            enforce_update: bool = False,
            is_based_on: list[State[Any]] = None,
            is_base_for: list[State[Any]] = None,
            **kwargs
    ) -> State[StateValueType]:

        if compare_fn is not None:
            compare_fn = BaseStates._wrap_compare_fn(compare_fn, **kwargs)
        state: State[StateValueType] = State[StateValueType](
            name,
            value=value,
            default_value=default_value,
            mapped_to_raw_fn=mapped_to_raw_fn,
            raw_to_mapped_fn=raw_to_mapped_fn,
            compare_fn=compare_fn,
            enforce_update=enforce_update,
            ignore_none=ignore_none,
            is_based_on=is_based_on,
            is_base_for=is_base_for,
        )
        self._states_dict[name] = state
        return state

    @staticmethod
    def _wrap_compare_fn(compare_fn, **kwargs) -> CompareFn:
        def _inner(before, after) -> bool:
            return compare_fn(before, after, **kwargs)

        return _inner
