from __future__ import annotations

import inspect
import time
from typing import Any, Callable, Final, Generic

import pyee

from dualsense_controller.state import CompareFn, ReadStateName, StateValueType
from dualsense_controller.state.common import MapFn, StateChangeCb, compare


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
    def on_change(self) -> Callable[[StateChangeCb], None]:
        return self._state.on_change

    @property
    def remove_change_listener(self) -> Callable[[StateChangeCb | None], None]:
        return self._state.remove_change_listener

    @property
    def remove_all_change_listeners(self) -> Callable[[], None]:
        return self._state.remove_all_change_listeners


class State(Generic[StateValueType]):

    def __init__(
            self,
            name: ReadStateName | str,
            # opts
            value: StateValueType = None,
            default_value: StateValueType = None,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn = None,
            enforce_update: bool = False,
            ignore_none: bool = True,
            depends_on: list[State[Any]] = None,
            is_dependency_of: list[State[Any]] = None,
    ):
        super().__init__()
        # CONST
        self.name: Final[ReadStateName] = name
        self._restricted_access: RestrictedStateAccess[StateValueType] | None = None
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()
        self._event_name_0_args: Final[str] = f'{name}_0'
        self._event_name_1_args: Final[str] = f'{name}_1'
        self._event_name_2_args: Final[str] = f'{name}_2'
        self._event_name_3_args: Final[str] = f'{name}_3'
        self._event_name_4_args: Final[str] = f'{name}_4'
        self._default_value: Final[StateValueType | None] = default_value
        self._depends_on: Final[list[State[StateValueType]]] = depends_on if depends_on is not None else []
        self._is_dependency_of: Final[list[State[StateValueType]]] = (
            is_dependency_of if is_dependency_of is not None else []
        )
        self._compare_fn: Final[CompareFn] = compare_fn if compare_fn is not None else compare
        self._mapped_to_raw_fn: Final[MapFn] = mapped_to_raw_fn
        self._raw_to_mapped_fn: Final[MapFn] = raw_to_mapped_fn
        self._ignore_none: Final[bool] = ignore_none
        self._enforce_update: Final[bool] = enforce_update
        # VAR
        self._value: StateValueType | None = value if value is not None else default_value
        self._change_timestamp: int = 0
        self._cycle_timestamp: int = 0
        self._last_value: StateValueType | None = None
        self._changed_since_last_update: bool = False

        for depends_on_state in self._depends_on:
            depends_on_state.add_as_dependecy_of(self)

        for is_dependency_of_state in self._is_dependency_of:
            is_dependency_of_state.add_depends_on(self)

    def set_value_without_triggering_change(self, new_value: StateValueType | None):
        self.set_value(new_value, trigger_change_on_changed=False)

    def set_value_mapped_without_triggering_change(self, new_value: StateValueType | None):
        self.set_value_mapped(new_value, trigger_change_on_changed=False)

    def set_value(
            self,
            value: StateValueType | None,
            trigger_change_on_changed: bool = True,
    ) -> None:
        old_value: StateValueType = self._value
        new_value: StateValueType = value
        if old_value is None and self._default_value is not None:
            old_value = self._default_value
        if new_value is None and self._default_value is not None:
            new_value = self._default_value
        if (old_value is None or new_value is None) and self._ignore_none:
            self.change_value(
                old_value=new_value,
                new_value=new_value,
                changed=False,
                trigger_change=False,
            )
            return
        changed, new_value = self._compare_fn(old_value, value)
        self.change_value(
            old_value=old_value,
            new_value=new_value,
            changed=changed,
            trigger_change=(changed if trigger_change_on_changed else False),
        )

    def set_value_mapped(
            self,
            vmapped: StateValueType | None,
            trigger_change_on_changed: bool = True,
    ) -> None:
        raw_val: StateValueType | None = vmapped if self._mapped_to_raw_fn is None else self._mapped_to_raw_fn(vmapped)
        # print(f'{self.name}: {vmapped} -> {raw_val}')
        self.set_value(raw_val, trigger_change_on_changed=trigger_change_on_changed)

    def change_value(
            self,
            old_value: StateValueType,
            new_value: StateValueType,
            changed: bool,
            trigger_change: bool = True,
    ) -> None:
        self._last_value = old_value
        self._value = new_value
        self._changed_since_last_update = changed
        self._change_timestamp = time.perf_counter_ns()
        if trigger_change:
            self._trigger_change()

    def set_cycle_timestamp(self, timestamp: int):
        self._cycle_timestamp = timestamp

    def _trigger_change(self):
        self._emit_change(self.last_value_mapped, self.value_mapped)

    def _emit_change(self, old_value: StateValueType, new_value: StateValueType):
        self._event_emitter.emit(self._event_name_0_args)
        self._event_emitter.emit(self._event_name_1_args, new_value)
        self._event_emitter.emit(self._event_name_2_args, new_value, self._change_timestamp)
        self._event_emitter.emit(self._event_name_3_args, old_value, new_value, self._change_timestamp)
        self._event_emitter.emit(self._event_name_4_args, self.name, old_value, new_value, self._change_timestamp)

    def __repr__(self) -> str:
        return f'State[{type(self.value).__name__}]({self.name}: {self.value})'

    # ################# PUBLIC ###############

    def trigger_change_if_changed(self) -> None:
        if self.has_changed:
            self._trigger_change()

    def add_as_dependecy_of(self, state: State[Any]):
        self._is_dependency_of.append(state)

    def add_depends_on(self, state: State[Any]):
        self._depends_on.append(state)

    def on_change(self, callback: StateChangeCb) -> None:
        self._event_emitter.on(
            self._get_event_name_by_callable(callback),
            callback
        )

    def remove_change_listener(self, callback: StateChangeCb | None = None) -> None:
        if callback is None:
            self.remove_all_change_listeners()
        else:
            self._event_emitter.remove_listener(
                self._get_event_name_by_callable(callback),
                callback
            )

    def _get_event_name_by_callable(self, callable_: Callable) -> str:
        num_params: int = len(inspect.signature(callable_).parameters)
        match num_params:
            case 0:
                return self._event_name_0_args
            case 1:
                return self._event_name_1_args
            case 2:
                return self._event_name_2_args
            case 3:
                return self._event_name_3_args
            case 4:
                return self._event_name_4_args
        raise Exception(f'invalid arg count {callable_}')

    def remove_all_change_listeners(self) -> None:
        self._event_emitter.remove_all_listeners()

    # ################# GETTERS AND SETTERS - OLDSCHOOL ###############

    def get_value(self) -> StateValueType:
        # if self._change_timestamp >= self._cycle_timestamp:
        #     return self._value
        # raise Exception('no current lavue')
        return self._value

    def get_last_value(self) -> StateValueType:
        return self._last_value

    def get_value_mapped(self) -> StateValueType:
        value: StateValueType = self.get_value()
        return value if not callable(self._raw_to_mapped_fn) else self._raw_to_mapped_fn(value)

    def get_last_value_mapped(self) -> StateValueType:
        last_value: StateValueType = self.get_last_value()
        return last_value if not callable(self._raw_to_mapped_fn) else self._raw_to_mapped_fn(last_value)

    # ################# GETTERS AND SETTERS ###############

    @property
    def value(self) -> StateValueType:
        return self.get_value()

    @property
    def last_value(self) -> StateValueType:
        return self.get_last_value()

    @property
    def value_mapped(self) -> StateValueType:
        return self.get_value_mapped()

    @property
    def last_value_mapped(self) -> StateValueType:
        return self.get_last_value_mapped()

    @property
    def enforce_update(self) -> bool:
        return self._enforce_update

    @property
    def restricted_access(self) -> RestrictedStateAccess[StateValueType]:
        if self._restricted_access is None:
            self._restricted_access = RestrictedStateAccess(self)
        return self._restricted_access

    @property
    def has_changed(self) -> bool:
        return self._changed_since_last_update

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
    def has_listeners(self) -> bool:
        return len(self._event_emitter.event_names()) > 0

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
