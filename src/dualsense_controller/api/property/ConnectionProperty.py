from functools import partial

from dualsense_controller.api.property.base import Property
from dualsense_controller.api.typedef import PropertyChangeCallback
from dualsense_controller.core.state.read_state.value_type import Connection


class ConnectionProperty(Property[Connection]):

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
