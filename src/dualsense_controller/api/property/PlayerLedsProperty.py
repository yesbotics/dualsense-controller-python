from dualsense_controller.api.property.base import Property
from dualsense_controller.core.state.write_state.enum import PlayerLedsBrightness, \
    PlayerLedsEnable
from dualsense_controller.core.state.write_state.value_type import PlayerLeds


class PlayerLedsProperty(Property[PlayerLeds]):

    def set_off(self) -> None:
        self._set_enable(PlayerLedsEnable.OFF)

    def set_center(self) -> None:
        self._set_enable(PlayerLedsEnable.CENTER)

    def set_inner(self) -> None:
        self._set_enable(PlayerLedsEnable.INNER)

    def set_outer(self) -> None:
        self._set_enable(PlayerLedsEnable.OUTER)

    def set_all(self) -> None:
        self._set_enable(PlayerLedsEnable.ALL)

    def set_center_and_outer(self) -> None:
        self._set_enable(PlayerLedsEnable.CENTER | PlayerLedsEnable.OUTER)

    def set_brightness_high(self) -> None:
        self._set_brightness(PlayerLedsBrightness.HIGH)

    def set_brightness_medium(self) -> None:
        self._set_brightness(PlayerLedsBrightness.MEDIUM)

    def set_brightness_low(self) -> None:
        self._set_brightness(PlayerLedsBrightness.LOW)

    def _set_enable(self, enable: PlayerLedsEnable):
        before: PlayerLeds = self._get_value()
        self._set_value(PlayerLeds(enable=enable, brightness=before.brightness))

    def _set_brightness(self, brightness: PlayerLedsBrightness):
        before: PlayerLeds = self._get_value()
        self._set_value(PlayerLeds(enable=before.enable, brightness=brightness))
