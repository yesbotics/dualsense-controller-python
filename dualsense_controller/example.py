from time import sleep
from typing import Any

from dualsense_controller import DualSenseController, ReadStateName, ConnectionType, WriteStateName


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
        self._dualsense_controller.on_state_change(ReadStateName.R2, self._on_btn_r2)
        self._dualsense_controller.on_state_change(ReadStateName.BTN_CROSS, self._on_btn_cross)

        self._dualsense_controller.on_any_state_change(self._on_any_state)

    def run(self) -> None:
        self._stay_alive = True
        self._dualsense_controller.init()
        sleep(1)
        print(self._dualsense_controller.read_states)
        sleep(1)
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

    def _on_btn_cross(self, _: bool, state: bool) -> None:
        if state:
            print(f'Cross Button pressed -> rumble')
            self._dualsense_controller.set_state(WriteStateName.MOTOR_RIGHT, 250)
        else:
            print(f'Cross Button released -> no rumble')
            self._dualsense_controller.set_state(WriteStateName.MOTOR_RIGHT, 0)


    def _on_btn_r2(self, _: bool, value: int) -> None:
        print(f'R2 Button value: {value}')

    def _on_any_state(self, name: ReadStateName, _: Any, state: Any) -> None:
        # print(f'{name}: {state}')
        pass


def main():
    Example().run()


if __name__ == "__main__":
    main()
