from typing import Final

from dualsense_controller.api.property import ButtonProperty, JoyStickProperty, RumbleProperty, TriggerProperty
from dualsense_controller.core.state.read_state.ReadStates import ReadStates
from dualsense_controller.core.state.write_state.WriteStates import WriteStates


class Properties:
    def __init__(
            self,
            read_states: ReadStates,
            write_states: WriteStates,
    ):
        # READ
        self.btn_cross: Final[ButtonProperty] = ButtonProperty(read_states.btn_cross)
        self.btn_square: Final[ButtonProperty] = ButtonProperty(read_states.btn_square)
        self.btn_triangle: Final[ButtonProperty] = ButtonProperty(read_states.btn_triangle)
        self.btn_circle: Final[ButtonProperty] = ButtonProperty(read_states.btn_circle)

        self.left_trigger: Final[TriggerProperty] = TriggerProperty(read_states.left_trigger)
        self.right_trigger: Final[TriggerProperty] = TriggerProperty(read_states.right_trigger)

        self.left_stick_x: Final[JoyStickProperty] = JoyStickProperty(read_states.left_stick_x)
        self.left_stick_y: Final[JoyStickProperty] = JoyStickProperty(read_states.left_stick_y)
        self.left_stick: Final[JoyStickProperty] = JoyStickProperty(read_states.left_stick)
        self.right_stick_x: Final[JoyStickProperty] = JoyStickProperty(read_states.right_stick_x)
        self.right_stick_y: Final[JoyStickProperty] = JoyStickProperty(read_states.right_stick_y)
        self.right_stick: Final[JoyStickProperty] = JoyStickProperty(read_states.right_stick)

        # WRITE
        self.left_rumble: Final[RumbleProperty] = RumbleProperty(write_states.left_motor)
        self.right_rumble: Final[RumbleProperty] = RumbleProperty(write_states.right_motor)
