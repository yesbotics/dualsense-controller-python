import warnings

from dualsense_controller.api.property.base import Property
from dualsense_controller.core.state.write_state.enum import LightbarPulseOptions
from dualsense_controller.core.state.write_state.value_type import Lightbar


class LightbarProperty(Property[Lightbar]):

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
