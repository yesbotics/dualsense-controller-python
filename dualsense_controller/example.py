from time import sleep
from typing import Any

from dualsense_controller import DualSenseController, ReadStateName, ConnectionType, WriteStateName
from dualsense_controller.common import OutPlayerLed


class Example:
    def __init__(self):
        self._stay_alive: bool = False

        self._dualsense_controller: DualSenseController = DualSenseController(
            device_index=0,
            analog_threshold=2,
            gyro_threshold=30,
            accelerometer_threshold=50,
        )

        self._dualsense_controller.on_exception(self._on_exception)
        self._dualsense_controller.on_connection_change(self._on_connection_change)

        self._dualsense_controller.on_state_change(ReadStateName.BTN_PS, self._on_btn_ps)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_L1, self._on_btn_l1)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_R1, self._on_btn_r1)
        self._dualsense_controller.on_state_change(ReadStateName.L2, self._on_l2)
        self._dualsense_controller.on_state_change(ReadStateName.R2, self._on_r2)

        self._dualsense_controller.on_state_change(ReadStateName.BTN_CROSS, self._on_btn_cross)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_SQUARE, self._on_btn_square)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_TRIANGLE, self._on_btn_triangle)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_CIRCLE, self._on_btn_circle)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_OPTIONS, self._on_btn_options)

        self._dualsense_controller.on_state_change(ReadStateName.BTN_LEFT, self._on_btn_left)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_UP, self._on_btn_up)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_RIGHT, self._on_btn_right)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_DOWN, self._on_btn_down)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_CREATE, self._on_btn_create)

        self._dualsense_controller.on_state_change(ReadStateName.BTN_MUTE, self._on_btn_mute)

        # 4 methods to get all state changes
        self._dualsense_controller.on_any_state_change(self._on_any_state)
        self._dualsense_controller.states.on_any_change(self._on_any_state_3)
        self._dualsense_controller.on_state_change(self._on_any_state_2)
        self._dualsense_controller.states.on_change(self._on_any_state_4)

        # 3 methods to get state changes of specific property
        self._dualsense_controller.on_state_change(ReadStateName.BTN_MUTE, self._on_btn_mute)
        self._dualsense_controller.states.on_change(ReadStateName.BTN_MUTE, self._on_btn_mute_2)
        self._dualsense_controller.states.btn_mute.on_change(self._on_btn_mute_3)

    def run(self) -> None:
        self._stay_alive = True
        self._dualsense_controller.init()
        while self._stay_alive:
            sleep(1)
        self._dualsense_controller.deinit()

    def _stop(self) -> None:
        self._stay_alive = False

    def _on_exception(self, exception: Exception) -> None:
        print(f'Oops! An exception occured: {exception} exit')
        self._stop()

    def _on_connection_change(self, connected: bool, connection_type: ConnectionType) -> None:
        print(f'Connection state changed. connected: {connected}, type: {connection_type}')

    def _on_btn_ps(self, _: bool, state: bool) -> None:
        print(f'PS Button pressed: {state}')
        if state is False:  # if stop holding ps key
            self._stop()

    def _on_btn_l1(self, _: bool, state: bool) -> None:
        print(f'L1 Button pressed: {state}')

    def _on_btn_r1(self, _: bool, state: bool) -> None:
        print(f'R1 Button pressed: {state}')

    def _on_l2(self, _: bool, value: int) -> None:
        self._dualsense_controller.set_state(WriteStateName.MOTOR_LEFT, value if value > 20 else 0)

    def _on_r2(self, _: bool, value: int) -> None:
        self._dualsense_controller.set_state(WriteStateName.MOTOR_RIGHT, value if value > 20 else 0)

    #
    # Left Controls -> lightbar color
    #
    def _on_btn_left(self, _: bool, state: bool) -> None:
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 0)

    def _on_btn_up(self, _: bool, state: bool) -> None:
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 0)

    def _on_btn_right(self, _: bool, state: bool) -> None:
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 255)

    def _on_btn_down(self, _: bool, state: bool) -> None:
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 255)

    def _on_btn_create(self, _: bool, state: bool) -> None:
        print(f"lightbar false")
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR, False)

    #
    # Right Controls -> Player LED
    #
    def _on_btn_square(self, _: bool, state: bool) -> None:
        print(f"player led center")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LED, OutPlayerLed.CENTER)

    def _on_btn_triangle(self, _: bool, state: bool) -> None:
        print(f"player led inner")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LED, OutPlayerLed.INNER)

    def _on_btn_circle(self, _: bool, state: bool) -> None:
        print(f"player led outer")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LED, OutPlayerLed.OUTER)

    def _on_btn_cross(self, _: bool, state: bool) -> None:
        print(f"player led all")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LED, OutPlayerLed.ALL)

    def _on_btn_options(self, _: bool, state: bool) -> None:
        print(f"player led off")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LED, OutPlayerLed.OFF)

    #
    #
    #
    def _on_btn_mute(self, _: bool, state: bool) -> None:
        print(f"mute")
        self._dualsense_controller.set_state(WriteStateName.MICROPHONE_LED, False)
    #
    # all
    #
    def _on_any_state(self, name: ReadStateName, _: Any, state: Any) -> None:
        # print(f'Any State {name}: {state}')
        pass

    def _on_any_state_2(self, name: ReadStateName, _: Any, state: Any) -> None:
        # print(f'Any State 2 {name}: {state}')
        pass

    def _on_any_state_3(self, name: ReadStateName, _: Any, state: Any) -> None:
        # print(f'Any State 3 {name}: {state}')
        pass

    def _on_any_state_4(self, name: ReadStateName, _: Any, state: Any) -> None:
        # print(f'Any State 4 {name}: {state}')
        pass

    def _on_btn_mute(self, _: bool, state: bool) -> None:
        print(f'Mute Button pressed: {state}')
        print(self._dualsense_controller.states.btn_mute.value)
        try:
            self._dualsense_controller.states.btn_mute.value = False
        except AttributeError:
            print('change the state from outside is not allowed.')

    def _on_btn_mute_2(self, _: bool, state: bool) -> None:
        print(f'Mute Button pressed 2: {state}')

    def _on_btn_mute_3(self, _: bool, state: bool) -> None:
        print(f'Mute Button pressed 3: {state}')


def main():
    Example().run()


if __name__ == "__main__":
    main()
