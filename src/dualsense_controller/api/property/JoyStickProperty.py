from dualsense_controller.api.property.base import Property
from dualsense_controller.core.state.read_state.value_type import JoyStick


class JoyStickProperty(Property[JoyStick]):

    @property
    def value(self) -> JoyStick:
        return self._get_value()
