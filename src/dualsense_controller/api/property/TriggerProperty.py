from typing import Final

from dualsense_controller.api.property.TriggerEffectProperty import TriggerEffectProperty
from dualsense_controller.api.property.TriggerFeedbackProperty import TriggerFeedbackProperty
from dualsense_controller.api.property.base import GetNumberProperty
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.typedef import Number


class TriggerProperty(GetNumberProperty):
    def __init__(
            self,
            trigger_value_state: State[Number],
            trigger_feedback_property: TriggerFeedbackProperty,
            trigger_effect_property: TriggerEffectProperty
    ):
        super().__init__(state=trigger_value_state)
        self._trigger_feedback_property: Final[TriggerFeedbackProperty] = trigger_feedback_property
        self._trigger_effect_property: Final[TriggerEffectProperty] = trigger_effect_property

    @property
    def feedback(self) -> TriggerFeedbackProperty:
        return self._trigger_feedback_property

    @property
    def effect(self) -> TriggerEffectProperty:
        return self._trigger_effect_property
