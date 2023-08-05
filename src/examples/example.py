import time

from dualsense_controller import DeviceInfo, DualSenseController, Number, JoyStick, Mapping, UpdateLevel


class Example:

    def __init__(self):
        self.is_running: bool = True
        device_infos: list[DeviceInfo] = DualSenseController.enumerate_devices()
        if len(device_infos) < 1:
            raise Exception('No DualSense Controller availabe.')
        first_device_info: DeviceInfo = device_infos[0]
        self.controller: DualSenseController = DualSenseController(
            device_index_or_device_info=first_device_info,
            mapping=Mapping.NORMALIZED,
            # update_level=UpdateLevel.DEFAULT,
            update_level=UpdateLevel.PAINSTAKING,
            # update_level=UpdateLevel.HAENGBLIEM,
        )
        self.controller.on_exception(self.on_exception)

        self.controller.btn_cross.on_down(self.on_btn_cross_down)

        # self.controller.btn_triangle.on_up(self.on_btn_triangle_up)
        # self.controller.btn_triangle.on_down(self.on_btn_triangle_down)
        # self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_1)
        # self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_2)
        # self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_3)
        #
        # self.controller.left_trigger.on_change(self.on_left_trigger_changed)
        # self.controller.right_trigger.on_change(self.on_right_trigger_changed)
        #
        self.controller.left_stick_x.on_change(self.on_left_stick_x_changed)
        self.controller.left_stick_y.on_change(self.on_left_stick_y_changed)
        self.controller.left_stick.on_change(self.on_left_stick_changed)
        self.controller.right_stick_x.on_change(self.on_right_stick_x_changed)
        self.controller.right_stick_y.on_change(self.on_right_stick_y_changed)
        self.controller.right_stick.on_change(self.on_right_stick_changed)

    def run(self) -> None:
        self.controller.start()
        while self.is_running:
            time.sleep(1)
        self.controller.stop()

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
