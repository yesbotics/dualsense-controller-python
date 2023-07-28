from time import sleep
from typing import Any

from dualsense_controller import (ConnectionType, DualSenseController, ReadStateName, StateValueMapping, WriteStateName)
from dualsense_controller.report import (OutBrightness, OutPlayerLed, OutPulseOptions)
from dualsense_controller.state import (
    Accelerometer,
    Gyroscope,
    JoyStick,
    Orientation
)


class Example:
    def __init__(self):
        self._stay_alive: bool = False

        self._dualsense_controller: DualSenseController = DualSenseController(
            # opts base
            device_index=0,
            # opts for feeling
            joystick_deadzone=10,
            shoulder_key_deadzone=2,
            gyroscope_threshold=100,
            accelerometer_threshold=100,
            orientation_threshold=100,
            # core opts
            state_value_mapping=StateValueMapping.FOR_NOOBS,
            # every loop update all values
            enforce_update=True,
            # trigger changes of a state after all subscribed states are updated
            trigger_change_after_all_values_set=True,

        )

        self._dualsense_controller.on_exception(self._on_exception)
        self._dualsense_controller.on_connection_change(self._on_connection_change)

        def xxx(_, n):
            print(n, self._dualsense_controller.states.btn_r1.value)

        self._dualsense_controller.states.btn_cross.on_change(xxx)

        # self._dualsense_controller.states.btn_ps.on_change(self._on_btn_ps)
        # self._dualsense_controller.states.btn_options.on_change(self._on_btn_options)
        # self._dualsense_controller.states.btn_create.on_change(self._on_btn_create)
        # self._dualsense_controller.states.btn_mute.on_change(self._on_btn_mute)
        #
        # self._dualsense_controller.states.btn_l1.on_change(self._on_btn_l1)
        # self._dualsense_controller.states.btn_r1.on_change(self._on_btn_r1)
        # self._dualsense_controller.states.l2.on_change(self._on_l2)
        # self._dualsense_controller.states.r2.on_change(self._on_r2)
        #
        # self._dualsense_controller.states.btn_cross.on_change(self._on_btn_cross)
        # self._dualsense_controller.states.btn_square.on_change(self._on_btn_square)
        # self._dualsense_controller.states.btn_triangle.on_change(self._on_btn_triangle)
        # self._dualsense_controller.states.btn_circle.on_change(self._on_btn_circle)
        #
        # self._dualsense_controller.states.btn_left.on_change(self._on_btn_left)
        # self._dualsense_controller.states.btn_up.on_change(self._on_btn_up)
        # self._dualsense_controller.states.btn_right.on_change(self._on_btn_right)
        # self._dualsense_controller.states.btn_down.on_change(self._on_btn_down)
        #
        # self._dualsense_controller.states.btn_r3.on_change(self._on_btn_r3)
        # self._dualsense_controller.states.btn_l3.on_change(self._on_btn_l3)
        #
        # # 4 methods to get all state changes
        # self._dualsense_controller.on_any_state_change(self._on_any_state)
        # self._dualsense_controller.states.on_any_change(self._on_any_state_3)
        # self._dualsense_controller.on_state_change(self._on_any_state_2)
        # self._dualsense_controller.states.on_change(self._on_any_state_4)
        #
        # # 3 methods to get state changes of specific property
        # self._dualsense_controller.on_state_change(ReadStateName.BTN_MUTE, self._on_btn_mute_1)
        # self._dualsense_controller.states.on_change(ReadStateName.BTN_MUTE, self._on_btn_mute_2)
        # self._dualsense_controller.states.btn_mute.on_change(self._on_btn_mute_3)
        #
        # # batt
        # self._dualsense_controller.on_battery_low(75, self._on_battery_low)
        #
        # # blubb
        # self._dualsense_controller.states.btn_options.on_change(self._on_btn_options)
        #
        # # touch
        # self._dualsense_controller.states.touch_0_x.on_change(self._on_touch_0)
        # self._dualsense_controller.states.touch_0_y.on_change(self._on_touch_0)
        #
        # # complex values
        # self._dualsense_controller.states.left_stick.on_change(self._on_left_stick)
        # self._dualsense_controller.states.right_stick.on_change(self._on_right_stick)
        # self._dualsense_controller.states.gyroscope.on_change(self._on_gyroscope)
        # self._dualsense_controller.states.accelerometer.on_change(self._on_accelerometer)
        # self._dualsense_controller.states.orientation.on_change(self._on_orientation)

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

    #
    # L1 / R1 -> brightness
    #
    def _on_btn_l1(self, _: bool, state: bool) -> None:
        print(f'L1 Button pressed: {state} -> brightness ')
        self._dualsense_controller.set_state(WriteStateName.BRIGHTNESS,
                                             OutBrightness.LOW if state else OutBrightness.HIGH)

    def _on_btn_r1(self, _: bool, state: bool) -> None:
        print(f'R1 Button pressed: {state}')
        self._dualsense_controller.set_state(WriteStateName.BRIGHTNESS,
                                             OutBrightness.MEDIUM if state else OutBrightness.HIGH)

    #
    # L2 / R2 -> rumble
    #
    def _on_l2(self, _: int, value: int) -> None:
        self._dualsense_controller.set_state(WriteStateName.MOTOR_LEFT, value)

    def _on_r2(self, _: int, value: int) -> None:
        self._dualsense_controller.set_state(WriteStateName.MOTOR_RIGHT, value)

    #
    # Left Controls -> lightbar color
    # Btn Create -> Lightbar off + Micro Mute
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
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR, state)
        self._dualsense_controller.set_state(WriteStateName.MICROPHONE_MUTE, state)

    #
    # Right Controls -> Player LED
    # Btn Options -> Player LED off + Micro LED
    #
    def _on_btn_square(self, _: bool, state: bool) -> None:
        print(f"player led center + outer")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LED, OutPlayerLed.CENTER | OutPlayerLed.OUTER)

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
        self._dualsense_controller.set_state(WriteStateName.MICROPHONE_LED, state)

    #
    # Microphone
    #
    def _on_btn_mute(self, _: bool, state: bool) -> None:
        print(f"mute")
        # self._dualsense_controller.set_state(WriteStateName.MICROPHONE_LED, state)
        # self._dualsense_controller.set_state(WriteStateName.MICROPHONE_MUTE, state)

    #
    # L3 / R3 -> led pulse modes
    #
    def _on_btn_r3(self, _: bool, state: bool) -> None:
        if state is False:
            print(f"R3 -> pulse FADE_OUT")
            self._dualsense_controller.set_state(WriteStateName.PULSE_OPTIONS, OutPulseOptions.FADE_OUT)

    def _on_btn_l3(self, _: bool, state: bool) -> None:
        if state is False:
            print(f"L3 -> pulse FADE_BLUE")
            self._dualsense_controller.set_state(WriteStateName.PULSE_OPTIONS, OutPulseOptions.FADE_BLUE)

    #
    # Touch0 x-value -> rgb-color
    #
    def _on_touch_0(self, _: bool, state: bool) -> None:
        x_max = 1920
        y_max = 1080
        x = self._dualsense_controller.states.touch_0_x.value
        y = self._dualsense_controller.states.touch_0_y.value
        x = min(x_max, max(0, x))
        y = min(y_max, max(0, y))

        color = int(0xffffff * x / x_max)
        red = (color >> 16) & 0xff
        green = (color >> 8) & 0xff
        blue = color & 0xff

        # print(f"Touch {x}-{y} -> color {hex(color)} {red}-{green}-{blue}")

        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, red)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, green)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, blue)

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

    #
    # misc
    #
    def _on_btn_mute_1(self, _: bool, state: bool) -> None:
        print(f'Mute Button pressed: {state}')
        if state:
            print(self._dualsense_controller.states.btn_mute.value)
            try:
                # noinspection PyPropertyAccess
                self._dualsense_controller.states.btn_mute.value = False
            except AttributeError:
                print('change the state from outside is not allowed.')
            print("batt lvl:", self._dualsense_controller.states.battery_level_percent.value)
            print("batt is full:", self._dualsense_controller.states.battery_full.value)
            print("batt is charging", self._dualsense_controller.states.battery_charging.value)

    def _on_btn_mute_2(self, _: bool, state: bool) -> None:
        print(f'Mute Button pressed 2: {state}')

    def _on_btn_mute_3(self, _: bool, state: bool) -> None:
        print(f'Mute Button pressed 3: {state}')

    def _on_battery_low(self, percentage: float) -> None:
        print(f'Battery is low: {percentage}')

    #
    # COMPLEX
    #
    def _on_left_stick(self, _: JoyStick, state: JoyStick) -> None:
        print(f'Left JoyStick: {state}')
        pass

    def _on_right_stick(self, _: JoyStick, state: JoyStick) -> None:
        print(f'Right JoyStick: {state}')
        pass

    def _on_gyroscope(self, _: Gyroscope, state: Gyroscope) -> None:
        # print(f'Gyroscope: {state}')
        pass

    def _on_accelerometer(self, _: Accelerometer, state: Accelerometer) -> None:
        # print(f'Accelerometer: {state}')
        pass

    def _on_orientation(self, _: Orientation, state: Orientation) -> None:
        # print(f'Orientation: {state}')
        pass


def main():
    Example().run()


if __name__ == "__main__":
    main()
