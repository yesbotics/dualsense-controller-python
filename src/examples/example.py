import time

from dualsense_controller import DeviceInfo, DualSenseController, JoyStick, Mapping, Number, UpdateLevel


class Example:

    def __init__(self):
        self.is_running: bool = True
        device_infos: list[DeviceInfo] = DualSenseController.enumerate_devices()
        if len(device_infos) < 1:
            raise Exception('No DualSense Controller availabe.')
        first_device_info: DeviceInfo = device_infos[0]
        self.controller: DualSenseController = DualSenseController(

            device_index_or_device_info=first_device_info,

            left_joystick_deadzone=0.1,
            right_joystick_deadzone=0.1,
            left_trigger_deadzone=0,
            right_trigger_deadzone=0,
            gyroscope_threshold=0,
            accelerometer_threshold=0,
            orientation_threshold=0,

            # mapping=Mapping.RAW,
            mapping=Mapping.NORMALIZED,

            # update_level=UpdateLevel.PAINSTAKING,
            # update_level=UpdateLevel.HAENGBLIEM,
            update_level=UpdateLevel.DEFAULT,
        )
        self.controller.exceptions.on_change(
            self.on_exception
        )
        # self.controller.benchmark.on_change(
        #     lambda res: print(f'on_update_benchmark: {res}')
        # )
        self.controller.connection.on_change(
            lambda res: print(f'on connection change: {res}')
        )
        self.controller.connection.on_connected(
            lambda conn_type: print(f'on connection connect: {conn_type}')
        )
        self.controller.connection.on_disconnected(
            lambda conn_type: print(f'on connection disconnect: {conn_type}')
        )
        self.controller.battery.on_change(
            lambda batt: print(f'on battery change: {batt}')
        )
        self.controller.battery.on_lower_than(
            100, lambda level: print(f'on battery low: {level}')
        )
        self.controller.battery.on_charging(
            lambda level: print(f'on battery charging: {level}')
        )
        self.controller.battery.on_discharging(
            lambda level: print(f'on battery discharging: {level}')
        )

        self.controller.btn_cross.on_down(self.on_btn_cross_down)

        # self.controller.btn_triangle.on_up(self.on_btn_triangle_up)
        # self.controller.btn_triangle.on_down(self.on_btn_triangle_down)
        # self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_1)
        # self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_2)
        # self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_3)

        self.controller.left_trigger.on_change(self.on_left_trigger_changed)
        self.controller.right_trigger.on_change(self.on_right_trigger_changed)

        self.controller.left_stick_x.on_change(self.on_left_stick_x_changed)
        self.controller.left_stick_y.on_change(self.on_left_stick_y_changed)
        self.controller.left_stick.on_change(self.on_left_stick_changed)
        self.controller.right_stick_x.on_change(self.on_right_stick_x_changed)
        self.controller.right_stick_y.on_change(self.on_right_stick_y_changed)
        self.controller.right_stick.on_change(self.on_right_stick_changed)

    def run(self) -> None:
        self.controller.activate()
        while self.is_running:
            time.sleep(1)
        self.controller.deactivate()

    def on_exception(self, exception: Exception) -> None:
        print(f'Exception occured:', exception)
        self.is_running = False

    def on_left_stick_x_changed(self, left_stick_x: Number):
        print(f'on_left_stick_x_changed: {left_stick_x}')

    def on_left_stick_y_changed(self, left_stick_y: Number):
        print(f'on_left_stick_y_changed: {left_stick_y}')

    def on_left_stick_changed(self, left_stick: JoyStick):
        print(f'on_left_stick_changed: {left_stick}')

    def on_right_stick_x_changed(self, right_stick_x: Number):
        print(f'on_right_stick_x_changed: {right_stick_x}')

    def on_right_stick_y_changed(self, right_stick_y: Number):
        print(f'on_right_stick_y_changed: {right_stick_y}')

    def on_right_stick_changed(self, right_stick: JoyStick):
        print(f'on_right_stick_changed: {right_stick}')

    def on_btn_triangle_up(self) -> None:
        print(f'Triangle button -> up')

    def on_btn_triangle_down(self) -> None:
        print(f'Triangle button -> down')

    def on_btn_triangle_changed_1(self, pressed: bool) -> None:
        print(f'Triangle button -> pressed: {pressed}')

    def on_btn_triangle_changed_2(self, pressed: bool, timestamp: int) -> None:
        print(f'Triangle button -> pressed: {pressed}, timestamp: {timestamp}')

    def on_btn_triangle_changed_3(self, last_pressed: bool, pressed: bool, timestamp: int) -> None:
        print(f'Triangle button -> last_pressed: {last_pressed}, pressed: {pressed}, timestamp: {timestamp}')

    def on_btn_cross_down(self) -> None:
        print(f'Cross button down')
        print(f'Get Square button. It is {self.controller.btn_square.pressed}')

    def on_left_trigger_changed(self, value: Number) -> None:
        print(f'L2 trigger: {value}')
        self.controller.left_rumble.value = value
        print(f'Left Rumble: {self.controller.left_rumble.value}')

    def on_right_trigger_changed(self, value: Number) -> None:
        print(f'L2 trigger: {value}')
        self.controller.right_rumble.value = value
        print(f'Right Rumble: {self.controller.right_rumble.value}')


def main():
    Example().run()


if __name__ == "__main__":
    main()
