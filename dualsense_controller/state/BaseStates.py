from typing import Any, Final, Generic

from dualsense_controller.state import CompareFn, MapFn, State, StateNameEnumType, \
    StateValueMapper, StateValueMapping, StateValueType


class BaseStates(Generic[StateNameEnumType]):

    def __init__(self, state_value_mapping: StateValueMapping):
        self._states_dict: Final[dict[StateNameEnumType, State]] = {}
        self._state_value_mapper: Final[StateValueMapper] = StateValueMapper(state_value_mapping)

    def set_value(self, name: StateNameEnumType, value: StateValueType, trigger_change: bool = True) -> None:
        state: State[StateValueType] = self._get_state_by_name(name)
        if not trigger_change:
            state.set_value_without_triggering_change(value)
        else:
            state.value = value

    def set_value_mapped(self, name: StateNameEnumType, value: StateValueType, trigger_change: bool = True) -> None:
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
            compare_fn: CompareFn[StateValueType] = None,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            depends_on: list[State[Any]] = None,
            is_dependency_of: list[State[Any]] = None,
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
            ignore_none=ignore_none,
            depends_on=depends_on,
            is_dependency_of=is_dependency_of,
        )
        self._states_dict[name] = state
        return state

    @staticmethod
    def _wrap_compare_fn(compare_fn, **kwargs) -> CompareFn:
        def _inner(before, after) -> bool:
            return compare_fn(before, after, **kwargs)

        return _inner
