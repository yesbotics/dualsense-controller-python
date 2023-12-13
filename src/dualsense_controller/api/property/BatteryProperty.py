from functools import partial

from dualsense_controller.api.property.base import Property
from dualsense_controller.api.typedef import PropertyChangeCallback
from dualsense_controller.core.state.read_state.value_type import Battery


class BatteryProperty(Property[Battery]):

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
