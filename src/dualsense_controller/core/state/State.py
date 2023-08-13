from __future__ import annotations

import time
from threading import Lock
from typing import Final, Generic

from dualsense_controller.core.core.Lockable import Lockable
from dualsense_controller.core.state.StateValueCallbackManager import StateValueCallbackManager
from dualsense_controller.core.state.mapping.typedef import MapFn
from dualsense_controller.core.state.typedef import CompareFn, CompareResult, StateChangeCallback, StateName, \
    StateValue


class State(Generic[StateValue]):

    @staticmethod
    def _compare(before: StateValue, after: StateValue) -> CompareResult:
        return (True, after) if before != after else (False, after)

    def __repr__(self) -> str:
        return f'State[{type(self._value_raw).__name__}]({self.name}: {self._value_raw} -> {self.value})'

    @property
    def value(self) -> StateValue:
        value_raw: StateValue = self.value_raw
        return value_raw if not callable(self._raw_to_mapped_fn) else self._raw_to_mapped_fn(value_raw)

    @value.setter
    def value(self, value_mapped: StateValue) -> None:
        self._set_value(value_mapped)

    @property
    def last_value(self) -> StateValue:
        last_value_raw: StateValue = self.last_value_raw
        return last_value_raw if not callable(self._raw_to_mapped_fn) else self._raw_to_mapped_fn(last_value_raw)

    @property
    def value_raw(self) -> StateValue:
        return self._value_raw

    @property
    def last_value_raw(self) -> StateValue:
        return self._last_value_raw

    @property
    def has_changed_since_last_set_value(self) -> bool:
        if self._disable_change_detection:
            return False
        return self._changed_since_last_set_value

    @property
    def has_listeners(self) -> bool:
        return self._callback_manager.has_listeners

    # LOCKED GETTERS AND SETTERS

    @property
    def _value_raw(self) -> StateValue:
        return self.__value.value

    @_value_raw.setter
    def _value_raw(self, _value: StateValue) -> None:
        self.__value.value = _value

    @property
    def _last_value_raw(self) -> StateValue:
        return self.__last_value.value

    @_last_value_raw.setter
    def _last_value_raw(self, _last_value: StateValue) -> None:
        self.__last_value.value = _last_value

    @property
    def _change_timestamp(self) -> int:
        return self.__change_timestamp.value

    @_change_timestamp.setter
    def _change_timestamp(self, _change_timestamp: int) -> None:
        self.__change_timestamp.value = _change_timestamp

    @property
    def _changed_since_last_set_value(self) -> bool:
        return self.__changed_since_last_update.value

    @_changed_since_last_set_value.setter
    def _changed_since_last_set_value(self, _changed_since_last_update: bool) -> None:
        self.__changed_since_last_update.value = _changed_since_last_update

    def __init__(
            self,
            name: StateName,
            value: StateValue = None,
            default_value: StateValue = None,
            ignore_none: bool = True,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn = None,
            disable_change_detection: bool = False,
    ):
        # CONST
        self.name: Final[StateName] = name
        self._lock: Final[Lock] = Lock()
        self._callback_manager: Final[StateValueCallbackManager[StateValue]] = StateValueCallbackManager(name)
        self._compare_fn: Final[CompareFn] = compare_fn if compare_fn is not None else State._compare
        self._mapped_to_raw_fn: Final[MapFn] = mapped_to_raw_fn
        self._raw_to_mapped_fn: Final[MapFn] = raw_to_mapped_fn
        self._ignore_none: Final[bool] = ignore_none
        self._default_value: Final[StateValue | None] = default_value
        self._disable_change_detection: Final[bool] = disable_change_detection

        # VAR
        self.__value: Lockable[StateValue | None] = Lockable(
            lock=self._lock,
            value=value if value is not None else default_value
        )
        self.__last_value: Lockable[StateValue | None] = Lockable(
            lock=self._lock,
            value=None
        )
        self.__change_timestamp: Lockable[int] = Lockable(
            lock=self._lock,
            value=0
        )
        self.__changed_since_last_update: Lockable[bool] = Lockable(
            lock=self._lock,
            value=False
        )

    def set_value_raw_without_triggering_change(self, new_value: StateValue | None):
        self._set_value_raw(new_value, trigger_change_on_changed=False)

    def set_value_without_triggering_change(self, new_value: StateValue | None):
        self._set_value(new_value, trigger_change_on_changed=False)

    def _set_value(
            self,
            value_mapped: StateValue | None,
            trigger_change_on_changed: bool = True,
    ) -> None:
        value_raw: StateValue | None = (
            value_mapped if self._mapped_to_raw_fn is None else self._mapped_to_raw_fn(value_mapped)
        )
        # print(f'{self.name}: {value_mapped} -> {raw_val}')
        self._set_value_raw(value_raw, trigger_change_on_changed=trigger_change_on_changed)

    def trigger_change_if_changed(self) -> None:
        if self.has_changed_since_last_set_value:
            self._trigger_change()

    def on_change(self, callback: StateChangeCallback) -> None:
        self._callback_manager.on_change(callback)

    def once_change(self, callback: StateChangeCallback) -> None:
        self._callback_manager.once_change(callback)

    def remove_change_listener(self, callback: StateChangeCallback | None = None) -> None:
        self._callback_manager.remove_change_listener(callback)

    def remove_all_change_listeners(self) -> None:
        self._callback_manager.remove_all_change_listeners()

    # ################# GETTERS AND SETTERS ###############

    def _set_value_raw(self, value_raw: StateValue | None, trigger_change_on_changed: bool = True) -> None:
        old_value: StateValue = self._value_raw
        new_value: StateValue = value_raw
        if old_value is None and self._default_value is not None:
            old_value = self._default_value
        if new_value is None and self._default_value is not None:
            new_value = self._default_value
        if self._ignore_none and (old_value is None or new_value is None):
            self._change_value(
                old_value=new_value,
                new_value=new_value,
                changed=False,
                trigger_change=False,
            )
            return
        changed, new_value = self._compare_fn(old_value, new_value)
        self._change_value(
            old_value=old_value,
            new_value=new_value,
            changed=changed,
            trigger_change=(changed if trigger_change_on_changed else False),
        )

    def _change_value(
            self,
            old_value: StateValue,
            new_value: StateValue,
            changed: bool,
            trigger_change: bool = True,
    ) -> None:
        self._last_value_raw = old_value
        self._value_raw = new_value
        self._change_timestamp = time.perf_counter_ns()
        self._changed_since_last_set_value = changed
        if not self._disable_change_detection and trigger_change:
            self._trigger_change()

    def _trigger_change(self):
        self._callback_manager.emit_change(self.last_value, self.value, self._change_timestamp)
