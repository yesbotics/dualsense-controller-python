from dataclasses import dataclass

from dualsense_controller.core.state.read_state.value_type import TriggerFeedback
from dualsense_controller.core.state.typedef import Number
from dualsense_controller.core.state.write_state.value_type import TriggerEffect


@dataclass(frozen=True, slots=True)
class Trigger:
    value: Number
    effect: TriggerEffect
    feedback: TriggerFeedback
