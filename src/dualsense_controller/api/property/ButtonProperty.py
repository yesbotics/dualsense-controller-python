from dualsense_controller.api.property.base import BoolProperty
from dualsense_controller.api.typedef import PropertyChangeCallback


class ButtonProperty(BoolProperty):

    def on_down(self, callback: PropertyChangeCallback):
        self._on_true(callback)

    def on_up(self, callback: PropertyChangeCallback):
        self._on_false(callback)

    @property
    def pressed(self) -> bool:
        return self._get_value()