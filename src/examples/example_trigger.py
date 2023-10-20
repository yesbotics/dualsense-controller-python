import time
import warnings

from dualsense_controller.api.DualSenseController import DualSenseController, Mapping
from dualsense_controller.api.enum import UpdateLevel
from dualsense_controller.api.property import TriggerProperty
from dualsense_controller.core.Benchmarker import Benchmark
from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.hidapi import DeviceInfo
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Connection, Gyroscope, \
    JoyStick, Orientation, TouchFinger
from dualsense_controller.core.state.typedef import Number


class ExampleTrigger:

    def __init__(self):
        self.controller: DualSenseController = DualSenseController(
            device_index_or_device_info=0,
        )

        self.left_trigger_effect_index: int = 0
        self.right_trigger_effect_index: int = 0
        self.trigger_effects_num: int = 20

        self.left_trigger_effects = [
            ["Continious resistence", self.controller.left_trigger.effect.set_continuous_resistance(), []]
        ]

        self.controller.btn_left.on_up(self.left_trigger_effect_previous)
        self.controller.btn_right.on_up(self.left_trigger_effect_next)
        # self.controller.btn_square.on_up(self.right_trigger_effect_previous)
        # self.controller.btn_circle.on_up(self.right_trigger_effect_next)

    def run(self) -> None:
        self.controller.activate()

        self.set_trigger_effect(self.controller.left_trigger, self.left_trigger_effect_index)
        self.set_trigger_effect(self.controller.right_trigger, self.right_trigger_effect_index)

        while True:
            time.sleep(1)
        self.controller.deactivate()

    # ############################################# MAIN ##################################################

    def left_trigger_effect_previous(self):
        self.left_trigger_effect_index = self.left_trigger_effect_index - 1 if self.left_trigger_effect_index > 0 else self.trigger_effects_num - 1
        self.set_trigger_effect(self.controller.left_trigger, self.left_trigger_effect_index)

    def left_trigger_effect_next(self):
        self.left_trigger_effect_index = self.left_trigger_effect_index + 1 if self.left_trigger_effect_index < (self.trigger_effects_num - 1) else 0
        self.set_trigger_effect(self.controller.left_trigger, self.left_trigger_effect_index)

    def set_trigger_effect(self, trigger: TriggerProperty, trigger_index: int):
        match trigger_index:
            case 0:
                print(f"Effect {trigger_index}: No resistance")
                trigger.effect.set_no_resistance()
            case 1:
                print(f"Effect {trigger_index}: Continious resistance: start: 0, force: 255")
                trigger.effect.set_continuous_resistance(0, 255)
            case 2:
                print(f"Effect {trigger_index}: Continious resistance: start: 127, force: 255")
                trigger.effect.set_continuous_resistance(127, 255)
            case 3:
                print(f"Effect {trigger_index}: Section resistance: start 0, 255")
                trigger.effect.set_section_resistance(0, 255)
            case 4:
                print(f"Effect {trigger_index}: Vibration: frequency: 100, off_time: 5")
                trigger.effect.set_vibrating(100, 5)
            case 5:
                print(f"Effect {trigger_index}: Bow: frequency: 127, off_time: 1")
                trigger.effect.set_bow(127, 0)

            case _:
                print(f"Effect: Index out of bound: {trigger_index}")


# ############################################# RUN EXAMPLE ##################################################

def main():
    ExampleTrigger().run()


if __name__ == "__main__":
    main()
