from __future__ import annotations

import inspect
from typing import Callable, Final, Generic

import pyee

from dualsense_controller.state import \
    AnyStateChangeCallback, \
    MappedStateValueType, ReadStateName, \
    StateChangeCallback, \
    StateValueType


class RestrictedStateAccess(Generic[StateValueType]):
    def __init__(self, state: State[StateValueType]):
        self._state = state

    @property
    def value(self) -> StateValueType | None:
        return self._state.value

    @property
    def changed(self) -> bool:
        return self._state.changed

    @property
    def last_value(self) -> StateValueType | None:
        return self._state.last_value

    @property
    def compare_fn(self) -> CompareFn:
        return self._state.compare_fn

    @compare_fn.setter
    def compare_fn(self, compare_fn: CompareFn) -> None:
        self._state.compare_fn = compare_fn

    @property
    def map_fn(self) -> MapFn:
        return self._state.map_fn

    @map_fn.setter
    def map_fn(self, map_fn: MapFn) -> None:
        self._state.map_fn = map_fn

    @property
    def on_change(self) -> Callable[[StateChangeCallback], None]:
        return self._state.on_change

    @property
    def remove_change_listener(self) -> Callable[[AnyStateChangeCallback | StateChangeCallback | None], None]:
        return self._state.remove_change_listener

    @property
    def remove_all_change_listeners(self) -> Callable[[], None]:
        return self._state.remove_all_change_listeners


CompareFn = Callable[[StateValueType, StateValueType, ...], StateValueType | None]
MapFn = Callable[[StateValueType], MappedStateValueType]


class State(Generic[StateValueType]):
    _DEFAULT_COMPARE_FN: Final[CompareFn[StateValueType]] = lambda before, after: before != after

    def __init__(
            self,
            name: ReadStateName,
            value: StateValueType = None,
            compare_fn: CompareFn = None,
            map_fn: MapFn[StateValueType] = None,
            ignore_initial_none: bool = True,
    ):
        super().__init__()
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()
        self.name: Final[ReadStateName] = name
        self._event_name_2_args: Final[str] = f'{name}_2'
        self._event_name_3_args: Final[str] = f'{name}_3'
        self._value: StateValueType | None = value
        self._last_value: StateValueType | None = None
        self._changed_since_last_update: bool = False
        self._restricted_access: RestrictedStateAccess[StateValueType] | None = None
        self._compare_fn: CompareFn = compare_fn if compare_fn is not None else State._DEFAULT_COMPARE_FN
        self._map_fn: MapFn | None = map_fn
        # extra
        self._ignore_initial_none: bool = ignore_initial_none

    @property
    def restricted_access(self) -> RestrictedStateAccess[StateValueType]:
        if self._restricted_access is None:
            self._restricted_access = RestrictedStateAccess(self)
        return self._restricted_access

    @property
    def has_listeners(self) -> bool:
        return len(self._event_emitter.event_names()) > 0

    def __repr__(self) -> str:
        return f'State[{type(self.value).__name__}]({self.name}: {self.value})'

    @property
    def compare_fn(self) -> CompareFn:
        return self._compare_fn

    @compare_fn.setter
    def compare_fn(self, compare_fn: CompareFn) -> None:
        self._compare_fn = compare_fn

    @property
    def map_fn(self) -> MapFn:
        return self._map_fn

    @map_fn.setter
    def map_fn(self, map_fn: MapFn) -> None:
        self._map_fn = map_fn

    @property
    def value(self) -> StateValueType:
        return self._value

    @value.setter
    def value(self, value: StateValueType | None) -> None:
        old_value: StateValueType = self._value
        if old_value is None and self._ignore_initial_none:
            self._change_value(old_value=value, new_value=value, changed=False, trigger_change=False)
            return
        if self._compare_fn(old_value, value):
            self._change_value(old_value=old_value, new_value=value)
            return
        self.do_not_change_value()

    @property
    def last_value(self) -> StateValueType:
        return self._last_value

    @property
    def changed(self) -> bool:
        return self._changed_since_last_update

    def set_value_without_triggering_change(self, new_value: StateValueType | None):
        self._change_value(old_value=self._value, new_value=new_value, changed=True, trigger_change=False)

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

    def _change_value(
            self,
            old_value: StateValueType,
            new_value: StateValueType,
            trigger_change: bool = True,
            changed: bool = True,
    ) -> None:
        self._last_value = old_value
        self._value = new_value
        self._changed_since_last_update = changed
        if trigger_change:
            self._event_emitter.emit(self._event_name_2_args, old_value, new_value)
            self._event_emitter.emit(self._event_name_3_args, self.name, old_value, new_value)

    def do_not_change_value(self) -> None:
        self._changed_since_last_update = False
