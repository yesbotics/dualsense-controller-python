import time

from dualsense_controller import DualSenseController, UpdateLevel, active_dualsense_controller, Mapping


class ContextManagerUsageExample:

    def run(self) -> None:
        controller: DualSenseController
        with active_dualsense_controller(
                left_joystick_deadzone=0.2,
                right_joystick_deadzone=0.2,
                left_trigger_deadzone=0.05,
                right_trigger_deadzone=0.05,
                gyroscope_threshold=0,
                accelerometer_threshold=0,
                orientation_threshold=0,
                mapping=Mapping.NORMALIZED,
                update_level=UpdateLevel.DEFAULT,
                microphone_initially_muted=True,
                microphone_invert_led=False,
        ) as controller:
            for i in range(0, 10):
                controller.wait_until_updated()
                print(controller.left_stick.value)
                time.sleep(1)


# ############################################# RUN EXAMPLE ##################################################

def main():
    ContextManagerUsageExample().run()


if __name__ == "__main__":
    main()
