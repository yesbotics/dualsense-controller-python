from abc import ABC
from functools import partial
from typing import Final, Generic

from dualsense_controller.core.Benchmarker import Benchmark
from dualsense_controller.core.report.out_report.enum import PlayerLeds
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Connection, Gyroscope, \
    JoyStick, Orientation, TouchFinger
from dualsense_controller.api.typedef import PropertyChangeCallback, PropertyType
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.typedef import Number


# BASE

class _Property(Generic[PropertyType], ABC):

    def __init__(self, state: State[PropertyType]):
        self._state: Final[State[PropertyType]] = state

    def on_change(self, callback: PropertyChangeCallback):
        self._state.on_change(callback)

    def once_change(self, callback: PropertyChangeCallback):
        self._state.once_change(callback)

    @property
    def changed(self) -> bool:
        return self._state.has_changed

    def _get_value(self) -> PropertyType:
        return self._state.value

    def _get_last_value(self) -> PropertyType:
        return self._state.last_value

    def _set_value(self, value: Number) -> None:
        self._state.value = value


class _GetNumberProperty(_Property[Number], ABC):

    @property
    def value(self) -> Number:
        return self._get_value()


class _GetSetNumberProperty(_Property[Number], ABC):

    @property
    def value(self) -> Number:
        return self._get_value()

    def set(self, value: Number):
        self._set_value(value)


class _BoolProperty(_Property[bool], ABC):

    def _on_true(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, True))

    def _on_false(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, False))

    @staticmethod
    def _on_changed(callback: PropertyChangeCallback, expected_value: bool, actual_value: bool):
        if expected_value == actual_value:
            callback()


# IMPL

class ButtonProperty(_BoolProperty):

    def on_down(self, callback: PropertyChangeCallback):
        self._on_true(callback)

    def on_up(self, callback: PropertyChangeCallback):
        self._on_false(callback)

    @property
    def pressed(self) -> bool:
        return self._get_value()


class TriggerProperty(_GetNumberProperty):
    pass


class RumbleProperty(_GetSetNumberProperty):
    pass


class JoyStickAxisProperty(_GetNumberProperty):
    pass


class JoyStickProperty(_Property[JoyStick]):

    @property
    def value(self) -> JoyStick:
        return self._get_value()


class ConnectionProperty(_Property[Connection]):

    @property
    def value(self) -> Connection:
        return self._get_value()

    def on_connected(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, True))

    def on_disconnected(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._on_changed, callback, False))

    @staticmethod
    def _on_changed(callback: PropertyChangeCallback, expected_value: bool, actual_value: Connection):
        if expected_value == actual_value.connected:
            callback(actual_value.connection_type)


class BenchmarkProperty(_Property[Benchmark]):

    @property
    def value(self) -> Benchmark:
        return self._get_value()


class ExceptionProperty(_Property[Exception]):

    @property
    def value(self) -> Exception:
        return self._get_value()


class BatteryProperty(_Property[Battery]):

    @property
    def value(self) -> Battery:
        return self._get_value()

    def on_lower_than(self, percentage: float, callback: PropertyChangeCallback):
        self.on_change(partial(self._check_low, callback, percentage))

    def on_charging(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._check_charging, callback, True))

    def on_discharging(self, callback: PropertyChangeCallback):
        self.on_change(partial(self._check_charging, callback, False))

    def _check_low(self, callback: PropertyChangeCallback, expected_value: float, actual_value: Battery):
        if (
                actual_value.level_percentage <= expected_value
                and (self._get_last_value() is None
                     or actual_value.level_percentage != self._get_last_value().level_percentage)
        ):
            callback(actual_value.level_percentage)

    def _check_charging(self, callback: PropertyChangeCallback, expected_value: bool, actual_value: Battery):
        if (
                expected_value == actual_value.charging
                and (self._get_last_value() is None
                     or actual_value.charging != self._get_last_value().charging)
        ):
            callback(actual_value.level_percentage)


class TouchFingerProperty(_Property[TouchFinger]):
    pass


class GyroscopeProperty(_Property[Gyroscope]):
    pass


class AccelerometerProperty(_Property[Accelerometer]):
    pass


class OrientationProperty(_Property[Orientation]):
    pass


class PlayerLedsProperty(_Property[PlayerLeds]):

    def set_off(self) -> None:
        self._set_value(PlayerLeds.OFF)

    def set_center(self) -> None:
        self._set_value(PlayerLeds.CENTER)

    def set_inner(self) -> None:
        self._set_value(PlayerLeds.INNER)

    def set_outer(self) -> None:
        self._set_value(PlayerLeds.OUTER)

    def set_all(self) -> None:
        self._set_value(PlayerLeds.ALL)

    def set_center_and_outer(self) -> None:
        self._set_value(PlayerLeds.CENTER | PlayerLeds.OUTER)
