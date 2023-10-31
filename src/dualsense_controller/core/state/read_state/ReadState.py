from __future__ import annotations

from typing import Any, Final, Generic

from dualsense_controller.core.core.Lockable import Lockable
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.mapping.typedef import MapFn
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.typedef import CompareFn, StateValue, StateValueFn


class ReadState(Generic[StateValue], State[StateValue]):

    @property
    def has_changed_dependencies(self) -> bool:
        return any(state.has_changed_since_last_set_value for state in self._depends_on)

    @property
    def has_changed_dependents(self) -> bool:
        return any(state.has_changed_since_last_set_value for state in self._is_dependency_of)

    @property
    def has_changed_dependencies_or_dependents(self) -> bool:
        return (
                any(state.has_changed_since_last_set_value for state in self._is_dependency_of)
                or any(state.has_changed_since_last_set_value for state in self._depends_on)
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

    @property
    def value_raw(self) -> StateValue:
        if self.is_self_updatable:
            return self.calc_value()
        return super().value_raw

    @property
    def is_self_updatable(self) -> bool:
        return self._can_update_itself and (self._cycle_timestamp > self._change_timestamp)

    @property
    def is_updatable_from_outside(self) -> bool:
        return (
                self._enforce_update
                or self.has_listeners
                or self.has_listened_dependents
                or self.has_changed_dependencies
        )

    def __init__(
            self,
            # BASE
            name: ReadStateName,
            value: StateValue = None,
            default_value: StateValue = None,
            ignore_none: bool = True,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn = None,

            # READ STATE
            value_calc_fn: StateValueFn = None,
            in_report_lockable: Lockable[InReport] = None,
            enforce_update: bool = False,
            can_update_itself: bool = True,
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
        # CONST
        self._depends_on: Final[list[ReadState[StateValue]]] = depends_on if depends_on is not None else []
        self._is_dependency_of: Final[list[ReadState[StateValue]]] = (
            is_dependency_of if is_dependency_of is not None else []
        )
        self._enforce_update: Final[bool] = enforce_update
        self._value_calc_fn: Final[StateValueFn] = value_calc_fn
        self._in_report_lockable: Final[Lockable[InReport]] = in_report_lockable
        self._can_update_itself: Final[bool] = can_update_itself

        # VAR
        self._cycle_timestamp: int = 0

        # AFTER
        for depends_on_state in self._depends_on:
            depends_on_state.add_as_dependecy_of(self)
        for is_dependency_of_state in self._is_dependency_of:
            is_dependency_of_state.add_depends_on(self)

    def calc_value(self, trigger_change_on_changed: bool = True) -> StateValue:
        value_raw: StateValue = self._value_calc_fn(
            self._in_report_lockable.value,
            *self._depends_on
        )
        self._set_value_raw(value_raw, trigger_change_on_changed)
        return self._value_raw

    def set_cycle_timestamp(self, timestamp: int):
        self._cycle_timestamp = timestamp

    def add_as_dependecy_of(self, state: ReadState[Any]):
        self._is_dependency_of.append(state)

    def add_depends_on(self, state: ReadState[Any]):
        self._depends_on.append(state)
