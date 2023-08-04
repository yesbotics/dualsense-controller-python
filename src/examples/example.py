import time

from dualsense_controller import DualSenseController, Number


class Example:

    def __init__(self):
        self.is_running: bool = True
        self.controller: DualSenseController = DualSenseController()
        self.controller.on_exception(self.on_exception)

        self.controller.btn_triangle.on_up(self.on_btn_triangle_up)
        self.controller.btn_triangle.on_down(self.on_btn_triangle_down)
        self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_1)
        self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_2)
        self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_3)

        self.controller.btn_cross.on_down(self.on_btn_cross_down)

        self.controller.left_trigger.on_change(self.on_left_trigger_changed)
        self.controller.right_trigger.on_change(self.on_right_trigger_changed)

    def run(self) -> None:
        self.controller.start()
        while self.is_running:
            time.sleep(1)
        self.controller.stop()

    def on_exception(self, exception: Exception) -> None:
        print(f'Exception occured:', exception)
        self.is_running = False

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
