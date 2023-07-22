from time import sleep
from typing import Any

from dualsense_controller import DualSenseController, StateName, ConnectionType


class Example:
    def __init__(self):
        self._stay_alive: bool = True

        self._dualsense_controller: DualSenseController = DualSenseController(
            device_index=0,
            # enable_connection_lookup=True,
            enable_connection_lookup=False,
            analog_threshold=2,
            gyro_threshold=1000,
            accelerometer_threshold=1000,
        )
        self._dualsense_controller.on_connection_change(self._on_connection_change)

        self._dualsense_controller.on_state_change(StateName.BTN_PS, self._on_btn_ps)
        self._dualsense_controller.on_state_change(StateName.BTN_L1, self._on_btn_l1)
        self._dualsense_controller.on_state_change(StateName.BTN_R1, self._on_btn_r1)

        self._dualsense_controller.on_any_state_change(self._on_any_state)

    def run(self) -> None:
        self._dualsense_controller.init()
        while self._stay_alive:
            sleep(1)
        self._dualsense_controller.deinit()

    def _on_connection_change(self, connected: bool, connection_type: ConnectionType) -> None:
        print(f'Connection state changed. connected: {connected}, type: {connection_type}')

    def _on_btn_ps(self, _: bool, state: bool) -> None:
        print(f'PS Button pressed: {state}')
        if state is True:
            self._stay_alive = False

    def _on_btn_l1(self, _: bool, state: bool) -> None:
        print(f'L1 Button pressed: {state}')

    def _on_btn_r1(self, _: bool, state: bool) -> None:
        print(f'R1 Button pressed: {state}')

    def _on_any_state(self, name: StateName, _: Any, state: Any) -> None:
        pass
        # print(f'{name}: {state}')


def main():
    Example().run()


if __name__ == "__main__":
    main()
