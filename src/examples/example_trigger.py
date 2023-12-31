import time

from dualsense_controller import DualSenseController, TriggerProperty


class ExampleTrigger:

    def __init__(self):
        self.controller: DualSenseController = DualSenseController(
            device_index_or_device_info=0,
        )

        self.trigger_effects = [
            lambda trigger: (
                print(f"Effect: no_resistance"),
                trigger.effect.no_resistance()
            ),
            lambda trigger: (
                print(f"Effect: off"),
                trigger.effect.off()
            ),
            lambda trigger: (
                print(f"Effect: continuous_resistance"),
                trigger.effect.continuous_resistance()
            ),
            lambda trigger: (
                print(f"Effect: feedback (full)"),
                trigger.effect.feedback()
            ),
            lambda trigger: (
                print(f"Effect: feedback (half)"),
                trigger.effect.feedback(strength=3)
            ),
            lambda trigger: (
                print(f"Effect: feedback (half,middle)"),
                trigger.effect.feedback(start_position=4, strength=3)
            ),
            lambda trigger: (
                print(f"Effect: section_resistance"),
                trigger.effect.section_resistance()
            ),
            lambda trigger: (
                print(f"Effect: weapon"),
                trigger.effect.weapon()
            ),
            lambda trigger: (
                print(f"Effect: multiple_position_feedback"),
                trigger.effect.multiple_position_feedback()
            ),
            lambda trigger: (
                print(f"Effect: slope_feedback"),
                trigger.effect.slope_feedback()
            ),
            lambda trigger: (
                print(f"Effect: bow"),
                trigger.effect.bow()
            ),
            lambda trigger: (
                print(f"Effect: galloping"),
                trigger.effect.galloping()
            ),
            lambda trigger: (
                print(f"Effect: machine"),
                trigger.effect.machine()
            ),
            lambda trigger: (
                print(f"Effect: simple_vibration"),
                trigger.effect.simple_vibration()
            ),
            lambda trigger: (
                print(f"Effect: full_press"),
                trigger.effect.full_press()
            ),
            lambda trigger: (
                print(f"Effect: soft_press"),
                trigger.effect.soft_press()
            ),
            lambda trigger: (
                print(f"Effect: medium_press"),
                trigger.effect.medium_press()
            ),
            lambda trigger: (
                print(f"Effect: hard_press"),
                trigger.effect.hard_press()
            ),
            lambda trigger: (
                print(f"Effect: pulse"),
                trigger.effect.pulse()
            ),
            lambda trigger: (
                print(f"Effect: choppy"),
                trigger.effect.choppy()
            ),
            lambda trigger: (
                print(f"Effect: soft_rigidity"),
                trigger.effect.soft_rigidity()
            ),
            lambda trigger: (
                print(f"Effect: medium_rigidity"),
                trigger.effect.medium_rigidity()
            ),
            lambda trigger: (
                print(f"Effect: max_rigidity"),
                trigger.effect.max_rigidity()
            ),
            lambda trigger: (
                print(f"Effect: half_press"),
                trigger.effect.half_press()
            ),
        ]
        self.trigger_effects_num: int = len(self.trigger_effects)
        self.left_trigger_effect_index: int = 0
        self.right_trigger_effect_index: int = 0

        self.controller.btn_left.on_up(self.left_trigger_effect_previous)
        self.controller.btn_right.on_up(self.left_trigger_effect_next)
        self.controller.btn_square.on_up(self.right_trigger_effect_previous)
        self.controller.btn_circle.on_up(self.right_trigger_effect_next)

    def run(self) -> None:
        self.controller.activate()

        self.set_trigger_effect(self.controller.left_trigger, self.left_trigger_effect_index)
        self.set_trigger_effect(self.controller.right_trigger, self.right_trigger_effect_index)

        while True:
            time.sleep(1)

    # ############################################# MAIN ##################################################

    def left_trigger_effect_previous(self):
        self.left_trigger_effect_index = (self.left_trigger_effect_index - 1) % self.trigger_effects_num
        self.set_trigger_effect(self.controller.left_trigger, self.left_trigger_effect_index)

    def left_trigger_effect_next(self):
        self.left_trigger_effect_index = (self.left_trigger_effect_index + 1) % self.trigger_effects_num
        self.set_trigger_effect(self.controller.left_trigger, self.left_trigger_effect_index)

    def right_trigger_effect_previous(self):
        self.right_trigger_effect_index = (self.right_trigger_effect_index - 1) % self.trigger_effects_num
        self.set_trigger_effect(self.controller.right_trigger, self.right_trigger_effect_index)

    def right_trigger_effect_next(self):
        self.right_trigger_effect_index = (self.right_trigger_effect_index + 1) % self.trigger_effects_num
        self.set_trigger_effect(self.controller.right_trigger, self.right_trigger_effect_index)

    def set_trigger_effect(self, trigger: TriggerProperty, trigger_index: int):
        self.trigger_effects[trigger_index](trigger)


# ############################################# RUN EXAMPLE ##################################################

def main():
    ExampleTrigger().run()


if __name__ == "__main__":
    main()
