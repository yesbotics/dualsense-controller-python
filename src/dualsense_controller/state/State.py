from __future__ import annotations

import inspect
import time
from typing import Final, Generic

import pyee

from dualsense_controller.state.mapping.typedef import MapFn
from dualsense_controller.state.typedef import CompareResult, StateChangeCallback, StateName, StateValueType, \
    CompareFn


class State(Generic[StateValueType]):

    @staticmethod
    def _compare(before: StateValueType, after: StateValueType) -> CompareResult:
        return (True, after) if before != after else (False, after)

    def __init__(
            self,
            name: StateName,
            # opts
            value: StateValueType = None,
            default_value: StateValueType = None,
            ignore_none: bool = True,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            compare_fn: CompareFn = None
    ):
        # CONST
        self.name: Final[StateName] = name
        self._changed_since_last_update: bool = False
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()
        self._event_name_0_args: Final[str] = f'{name}_0'
        self._event_name_1_args: Final[str] = f'{name}_1'
        self._event_name_2_args: Final[str] = f'{name}_2'
        self._event_name_3_args: Final[str] = f'{name}_3'
        self._event_name_4_args: Final[str] = f'{name}_4'
        self._compare_fn: Final[CompareFn] = compare_fn if compare_fn is not None else State._compare
        self._mapped_to_raw_fn: Final[MapFn] = mapped_to_raw_fn
        self._raw_to_mapped_fn: Final[MapFn] = raw_to_mapped_fn
        self._ignore_none: Final[bool] = ignore_none
        # VAR
        self._value: StateValueType | None = value if value is not None else default_value
        self._change_timestamp: int = 0
        self._cycle_timestamp: int = 0
        self._last_value: StateValueType | None = None

        self._default_value: Final[StateValueType | None] = default_value

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

    def on_change(self, callback: StateChangeCallback) -> None:
        self._event_emitter.on(
            self._get_event_name_by_callable(callback),
            callback
        )

    def remove_change_listener(self, callback: StateChangeCallback | None = None) -> None:
        if callback is None:
            self.remove_all_change_listeners()
        else:
            self._event_emitter.remove_listener(
                self._get_event_name_by_callable(callback),
                callback
            )

    def _get_event_name_by_callable(self, callable_: StateChangeCallback) -> str:
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
    def has_changed(self) -> bool:
        return self._changed_since_last_update

    @property
    def has_listeners(self) -> bool:
        return len(self._event_emitter.event_names()) > 0
