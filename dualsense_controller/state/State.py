from __future__ import annotations

import inspect
from typing import Any, Callable, Final, Generic

import pyee

from dualsense_controller.state import \
    AnyStateChangeCallback, \
    CompareFn, ReadStateName, \
    StateChangeCallback, \
    StateValueType
from dualsense_controller.state.common import MapFn, compare


class RestrictedStateAccess(Generic[StateValueType]):
    def __init__(self, state: State[StateValueType]):
        self._state = state

    @property
    def value(self) -> StateValueType | None:
        return self._state.value_mapped

    @property
    def changed(self) -> bool:
        return self._state.changed

    @property
    def last_value(self) -> StateValueType | None:
        return self._state.last_value_mapped

    @property
    def on_change(self) -> Callable[[StateChangeCallback], None]:
        return self._state.on_change

    @property
    def enforce_update(self) -> bool:
        return self._state.enforce_update

    @property
    def remove_change_listener(self) -> Callable[[AnyStateChangeCallback | StateChangeCallback | None], None]:
        return self._state.remove_change_listener

    @property
    def remove_all_change_listeners(self) -> Callable[[], None]:
        return self._state.remove_all_change_listeners


class State(Generic[StateValueType]):

    def __init__(
            self,
            name: ReadStateName,
            # opts
            value: StateValueType = None,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn = None,
            ignore_none: bool = True,
            enforce_update: bool = False,
            is_based_on: list[State[Any]] = None,
            is_base_for: list[State[Any]] = None,
    ):
        super().__init__()
        self.name: Final[ReadStateName] = name
        self._restricted_access: RestrictedStateAccess[StateValueType] | None = None
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()
        self._event_name_2_args: Final[str] = f'{name}_2'
        self._event_name_3_args: Final[str] = f'{name}_3'
        self._value: StateValueType | None = value
        self._last_value: StateValueType | None = None
        # opts
        self._is_based_on: list[State[StateValueType]] = is_based_on if is_based_on is not None else []
        self._is_base_for: list[State[StateValueType]] = is_base_for if is_base_for is not None else []
        self._enforce_update: bool = enforce_update
        self._changed_since_last_update: bool = False
        self._compare_fn: CompareFn = compare_fn if compare_fn is not None else compare
        self._mapped_to_raw_fn: MapFn = mapped_to_raw_fn
        self._raw_to_mapped_fn: MapFn = raw_to_mapped_fn
        self._ignore_none: bool = ignore_none

        for based_on_state in self._is_based_on:
            based_on_state.set_as_base_for(self)

    # ################# PRIVATE ###############

    def _set_value(
            self,
            value: StateValueType | None,
            trigger_change_on_changed: bool = True,
    ) -> None:
        old_value: StateValueType = self._value
        new_value: StateValueType = value
        if (old_value is None or new_value is None) and self._ignore_none:
            self._change_value(old_value=new_value, new_value=new_value, changed=False, trigger_change=False)
            return
        changed, new_value = self._compare_fn(old_value, value)
        self._change_value(
            old_value=old_value,
            new_value=new_value,
            changed=changed,
            trigger_change=(changed if trigger_change_on_changed else False)
        )

    def _change_value(
            self,
            old_value: StateValueType,
            new_value: StateValueType,
            changed: bool,
            trigger_change: bool,
    ) -> None:
        self._last_value = old_value
        self._value = new_value
        self._changed_since_last_update = changed
        if trigger_change:
            self._trigger_change()

    def _trigger_change(self):
        # self._emit_change(self.last_value, self._value)
        self._emit_change(self.last_value_mapped, self.value_mapped)

    def _emit_change(self, old_value: StateValueType, new_value: StateValueType):
        self._event_emitter.emit(self._event_name_2_args, old_value, new_value)
        self._event_emitter.emit(self._event_name_3_args, self.name, old_value, new_value)

    def __repr__(self) -> str:
        return f'State[{type(self.value).__name__}]({self.name}: {self.value})'

    # ################# PUBLIC ###############

    def trigger_change_if_changed(self) -> None:
        if self.changed:
            self._trigger_change()

    def set_as_base_for(self, state: State[Any]):
        self._is_base_for.append(state)

    def set_value_without_triggering_change(self, new_value: StateValueType | None):
        self._set_value(new_value, trigger_change_on_changed=False)

    def on_change(self, callback: AnyStateChangeCallback | StateChangeCallback) -> None:
        num_params: int = len(inspect.signature(callback).parameters)
        self._event_emitter.on(
            self._event_name_2_args if num_params == 2 else self._event_name_3_args,
            callback
        )

    def remove_change_listener(self, callback: AnyStateChangeCallback | StateChangeCallback | None = None) -> None:
        if callback is None:
            self.remove_all_change_listeners()
        else:
            num_params: int = len(inspect.signature(callback).parameters)
            self._event_emitter.remove_listener(
                self._event_name_2_args if num_params == 2 else self._event_name_3_args,
                callback
            )

    def remove_all_change_listeners(self) -> None:
        self._event_emitter.remove_all_listeners()

    # ################# GETTERS AND SETTERS ###############

    @property
    def value(self) -> StateValueType:
        return self._value

    @value.setter
    def value(self, value: StateValueType | None) -> None:
        self._set_value(value)

    @property
    def last_value(self) -> StateValueType:
        return self._last_value

    @property
    def value_mapped(self) -> StateValueType:
        return self.value if not callable(self._raw_to_mapped_fn) else self._raw_to_mapped_fn(self._value)

    @value_mapped.setter
    def value_mapped(self, value: StateValueType | None) -> None:
        self.value = value if self._mapped_to_raw_fn is None else self._mapped_to_raw_fn(value)

    @property
    def last_value_mapped(self) -> StateValueType:
        return self._last_value if not callable(self._raw_to_mapped_fn) else self._raw_to_mapped_fn(self._last_value)

    @property
    def restricted_access(self) -> RestrictedStateAccess[StateValueType]:
        if self._restricted_access is None:
            self._restricted_access = RestrictedStateAccess(self)
        return self._restricted_access

    @property
    def is_updatable(self) -> bool:
        return (
                self.enforce_update
                or (len(self._is_based_on) == 0 and self.has_listeners)
                or (self.has_listeners and any(state.changed for state in self._is_based_on))
        )

    @property
    def has_listeners_self_only(self) -> bool:
        return len(self._event_emitter.event_names()) > 0

    @property
    def has_listeners(self) -> bool:
        return (
                self.has_listeners_self_only
                or any(state.has_listeners_self_only for state in self._is_base_for)
                or any(state.has_listeners for state in self._is_based_on)
        )

    @property
    def enforce_update_self_only(self) -> bool:
        return self._enforce_update

    @property
    def enforce_update(self) -> bool:
        return (
                self.enforce_update_self_only
                or any(state.enforce_update_self_only for state in self._is_base_for)
                or any(state.enforce_update for state in self._is_based_on)
        )

    @property
    def changed(self) -> bool:
        return self._changed_since_last_update
