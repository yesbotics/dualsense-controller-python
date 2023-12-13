from dualsense_controller.api.property.base import Property


class ExceptionProperty(Property[Exception]):

    @property
    def value(self) -> Exception:
        return self._get_value()
