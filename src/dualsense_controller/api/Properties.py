from typing import Final

from dualsense_controller.api.property import ButtonProperty, TriggerProperty
from dualsense_controller.core.state.read_state.ReadStates import ReadStates
from dualsense_controller.core.state.write_state.WriteStates import WriteStates


class Properties:
    def __init__(
            self,
            read_states: ReadStates,
            write_states: WriteStates,
    ):
        self.btn_cross: Final[ButtonProperty] = ButtonProperty(read_states.btn_cross)
        self.btn_square: Final[ButtonProperty] = ButtonProperty(read_states.btn_square)
        self.btn_triangle: Final[ButtonProperty] = ButtonProperty(read_states.btn_triangle)
        self.btn_circle: Final[ButtonProperty] = ButtonProperty(read_states.btn_circle)
        self.left_trigger: Final[TriggerProperty] = TriggerProperty(read_states.l2)
        self.right_trigger: Final[TriggerProperty] = TriggerProperty(read_states.r2)
        # self.left_rumble: Final[RumbleProperty] = RumbleProperty(write_states.left_rumble)
        # self.right_rumble: Final[RumbleProperty] = RumbleProperty(read_states.right_rumble)
