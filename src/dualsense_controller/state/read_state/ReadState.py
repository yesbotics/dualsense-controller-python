from __future__ import annotations

from typing import Any, Final, Generic

from dualsense_controller.state.State import State
from dualsense_controller.state.mapping.typedef import MapFn
from dualsense_controller.state.read_state.enum import ReadStateName
from dualsense_controller.state.typedef import StateValueType, CompareFn


class ReadState(Generic[StateValueType], State[StateValueType]):

    @property
    def enforce_update(self) -> bool:
        return self._enforce_update

    @property
    def has_changed_dependencies(self) -> bool:
        return any(state.has_changed for state in self._depends_on)

    @property
    def has_changed_dependents(self) -> bool:
        return any(state.has_changed for state in self._is_dependency_of)

    @property
    def has_changed_dependencies_or_dependents(self) -> bool:
        return (
                any(state.has_changed for state in self._is_dependency_of)
                or any(state.has_changed for state in self._depends_on)
        )

    @property
    def has_listened_dependencies_or_dependents(self) -> bool:
        return (
                any(state.has_listeners for state in self._is_dependency_of)
                or any(state.has_listeners for state in self._depends_on)
        )

    @property
    def has_listened_dependents(self) -> bool:
        return any(state.has_listeners for state in self._is_dependency_of)

    @property
    def has_listened_dependencies(self) -> bool:
        return any(state.has_listeners for state in self._depends_on)

    def __init__(
            self,
            name: ReadStateName,
            # opts
            value: StateValueType = None,
            default_value: StateValueType = None,
            ignore_none: bool = True,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn = None,
            enforce_update: bool = False,
            depends_on: list[State[Any]] = None,
            is_dependency_of: list[State[Any]] = None,
    ):
        State.__init__(
            self,
            name=name,
            value=value,
            default_value=default_value,
            ignore_none=ignore_none,
            mapped_to_raw_fn=mapped_to_raw_fn,
            raw_to_mapped_fn=raw_to_mapped_fn,
            compare_fn=compare_fn,
        )
        self._depends_on: Final[list[ReadState[StateValueType]]] = depends_on if depends_on is not None else []
        self._is_dependency_of: Final[list[ReadState[StateValueType]]] = (
            is_dependency_of if is_dependency_of is not None else []
        )
        self._enforce_update: Final[bool] = enforce_update

        for depends_on_state in self._depends_on:
            depends_on_state.add_as_dependecy_of(self)

        for is_dependency_of_state in self._is_dependency_of:
            is_dependency_of_state.add_depends_on(self)

    def add_as_dependecy_of(self, state: ReadState[Any]):
        self._is_dependency_of.append(state)

    def add_depends_on(self, state: ReadState[Any]):
        self._depends_on.append(state)
