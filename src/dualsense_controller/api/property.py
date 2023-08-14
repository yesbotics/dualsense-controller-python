import warnings
from abc import ABC
from copy import copy
from dataclasses import dataclass
from functools import partial
from typing import Any, Final, Generic

from dualsense_controller.core.Benchmarker import Benchmark
from dualsense_controller.core.report.out_report.enum import LightbarPulseOptions, PlayerLeds
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Connection, Gyroscope, \
    JoyStick, Orientation, TouchFinger
from dualsense_controller.api.typedef import PropertyChangeCallback, PropertyType
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.typedef import Number
from dualsense_controller.core.state.write_state.value_type import Lightbar, Microphone


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
        return self._state.has_changed_since_last_set_value

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

    def set_brightess(self) -> None:
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


class MicrophoneProperty(_Property[Microphone]):

    def __init__(
            self,
            state: State[Microphone],
            invert_led: bool = False
    ):
        super().__init__(state)
        self._invert_led: Final[bool] = invert_led

    def toggle_muted(self) -> None:
        if self.is_muted:
            self.set_unmuted()
        else:
            self.set_muted()

    def set_muted(self) -> None:
        self._set_mute(True)

    def set_unmuted(self) -> None:
        self._set_mute(False)

    def refresh_workaround(self) -> None:
        warnings.warn("Micrphone state initially not set properly. workaround enforces it", UserWarning)
        self.toggle_muted()
        self.toggle_muted()

    def _set_mute(self, mute: bool):
        self._set_value(Microphone(
            mute=mute,
            led=(mute if not self._invert_led else not mute)
        ))

    @property
    def is_muted(self) -> bool:
        return self._get_value().mute


class LightbarProperty(_Property[Lightbar]):

    @property
    def color(self) -> tuple[int, int, int]:
        current: Lightbar = self._get_value()
        return current.red, current.green, current.blue

    @property
    def is_on(self) -> bool:
        return self._get_value().is_on

    def fade_in_blue(self) -> None:
        self._set(pulse_options=LightbarPulseOptions.FADE_IN_BLUE)

    def fade_out_blue(self) -> None:
        self._set(pulse_options=LightbarPulseOptions.FADE_OUT_BLUE)

    def set_on(self) -> None:
        self.set_is_on(True)

    def set_off(self) -> None:
        self.set_is_on(False)

    def toggle_on_off(self) -> None:
        self.set_is_on(not self.is_on)

    def set_is_on(self, is_on: bool) -> None:
        self._set(is_on=is_on)

    def set_color(self, red: int, green: int, blue: int) -> None:
        self._set(red=red, green=green, blue=blue)

    def set_color_black(self) -> None:
        self.set_color(0, 0, 0)

    def set_color_white(self) -> None:
        self.set_color(255, 255, 255)

    def set_color_red(self) -> None:
        self.set_color(255, 0, 0)

    def set_color_green(self) -> None:
        self.set_color(0, 255, 0)

    def set_color_blue(self) -> None:
        self.set_color(0, 0, 255)

    def _set(
            self,
            red: int = None,
            green: int = None,
            blue: int = None,
            is_on: int = None,
            pulse_options: int = None,
    ):
        before: Lightbar = self._get_value()
        if (
                before.pulse_options == LightbarPulseOptions.FADE_IN_BLUE
                and pulse_options is None
        ):
            warnings.warn('currently lightbar set to fade_in_blue. '
                          'other actions like changing color are not possible. '
                          'set fade_out_blue to change other colors')
        self._set_value(Lightbar(
            red=red if red is not None else before.red,
            green=green if green is not None else before.green,
            blue=blue if blue is not None else before.blue,
            is_on=is_on if is_on is not None else before.is_on,
            pulse_options=pulse_options if pulse_options is not None else before.pulse_options,
        ))
