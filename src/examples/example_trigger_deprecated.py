import time

from dualsense_controller import DualSenseController, TriggerProperty


class ExampleTrigger:

    def __init__(self):
        self.controller: DualSenseController = DualSenseController(
            device_index_or_device_info=0,
        )

        self.trigger_effects = [
            lambda trigger: (
                print(f"Effect: set_no_resistance"),
                trigger.effect.set_no_resistance()
            ),
            lambda trigger: (
                print(f"Effect: set_continuous_resistance, start_pos: 0, force: 255"),
                trigger.effect.set_continuous_resistance(0, 255)
            ),
            lambda trigger: (
                print(f"Effect: set_continuous_resistance, start_pos: 127, force: 255"),
                trigger.effect.set_continuous_resistance(127, 255)
            ),
            lambda trigger: (
                print(f"Effect: set_section_resistance, start_pos: 0, endpos: 100, force: 255"),
                trigger.effect.set_section_resistance(0, 100, 255)
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
