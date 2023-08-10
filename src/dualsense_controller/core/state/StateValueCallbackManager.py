import inspect
from typing import Final, Generic

import pyee

from dualsense_controller.core.state.typedef import StateChangeCallback, StateName, StateValue


class StateValueCallbackManager(Generic[StateValue]):

    @property
    def has_listeners(self) -> bool:
        return len(self._event_emitter.event_names()) > 0

    def __init__(self, name: StateName):
        self._name: Final[StateName] = name
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()

        self._event_name_0_args: Final[str] = f'{name}_0'
        self._event_name_1_args: Final[str] = f'{name}_1'
        self._event_name_2_args: Final[str] = f'{name}_2'
        self._event_name_3_args: Final[str] = f'{name}_3'
        self._event_name_4_args: Final[str] = f'{name}_4'

    def on_change(self, callback: StateChangeCallback) -> None:
        self._event_emitter.on(self._get_event_name_by_callable(callback), callback)

    def once_change(self, callback: StateChangeCallback) -> None:
        self._event_emitter.once(self._get_event_name_by_callable(callback), callback)

    def remove_change_listener(self, callback: StateChangeCallback | None = None) -> None:
        if callback is None:
            self.remove_all_change_listeners()
        else:
            self._event_emitter.remove_listener(
                self._get_event_name_by_callable(callback),
                callback
            )

    def remove_all_change_listeners(self) -> None:
        self._event_emitter.remove_all_listeners()

    def emit_change(self, old_value: StateValue, new_value: StateValue, timestamp: int):
        if self._event_name_0_args in self._event_emitter.event_names():
            self._event_emitter.emit(self._event_name_0_args)
        if self._event_name_1_args in self._event_emitter.event_names():
            self._event_emitter.emit(self._event_name_1_args, new_value)
        if self._event_name_2_args in self._event_emitter.event_names():
            self._event_emitter.emit(self._event_name_2_args, new_value, timestamp)
        if self._event_name_3_args in self._event_emitter.event_names():
            self._event_emitter.emit(self._event_name_3_args, old_value, new_value, timestamp)
        if self._event_name_4_args in self._event_emitter.event_names():
            self._event_emitter.emit(self._event_name_4_args, self._name, old_value, new_value, timestamp)

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
