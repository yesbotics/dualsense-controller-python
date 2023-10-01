import time
import warnings

from dualsense_controller.api.DualSenseController import DualSenseController, Mapping
from dualsense_controller.api.enum import UpdateLevel
from dualsense_controller.core.Benchmarker import Benchmark
from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.hidapi import DeviceInfo
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Connection, Gyroscope, \
    JoyStick, Orientation, TouchFinger
from dualsense_controller.core.state.typedef import Number


class ExampleTrigger:

    def __init__(self):
        self.controller: DualSenseController = DualSenseController(
            device_index_or_device_info=1,
        )

    def run(self) -> None:
        self.controller.activate()

        self.controller.left_trigger.effect.set_continuous_resistance(0, 255)
        # self.controller.right_trigger.effect.set_continuous_resistance(0, 128)

        for i in range(0,255):
            self.controller.left_trigger.effect.set_continuous_resistance(120, i)
            print(f'Force: {i}')
            time.sleep(0.2)

        while True:
            time.sleep(1)
        self.controller.deactivate()

    # ############################################# MAIN ##################################################


# ############################################# RUN EXAMPLE ##################################################

def main():
    ExampleTrigger().run()


if __name__ == "__main__":
    main()
