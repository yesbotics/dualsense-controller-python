import warnings
from typing import Final

from dualsense_controller.api.property.base import Property
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.write_state.value_type import Microphone


class MicrophoneProperty(Property[Microphone]):

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
        warnings.warn("Microphone state initially not set properly. workaround enforces it", UserWarning)
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
