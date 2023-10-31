from time import sleep
from typing import Any

from dualsense_controller.core.DualSenseControllerCore import DualSenseControllerCore
from dualsense_controller.core.state.mapping.enum import StateValueMapping
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Connection, Gyroscope, JoyStick, \
    Orientation, \
    TouchFinger
from dualsense_controller.core.state.write_state.enum import WriteStateName, PlayerLedsBrightness, PlayerLedsEnable, \
    LightbarPulseOptions


class CoreExample:
    def __init__(self):
        self._stay_alive: bool = False

        self._dualsense_controller: DualSenseControllerCore = DualSenseControllerCore(
            # ##### BASE  #####
            device_index_or_device_info=0,
            # ##### FEELING  #####
            left_joystick_deadzone=.1,
            right_joystick_deadzone=.1,
            left_trigger_deadzone=.1,
            right_trigger_deadzone=.1,
            gyroscope_threshold=0,
            accelerometer_threshold=0,
            orientation_threshold=0,
            state_value_mapping=StateValueMapping.NORMALIZED,
            # ##### CORE #####
            enforce_update=False,
            can_update_itself=True,
        )

        self._dualsense_controller.exception_state.on_change(self._on_exception)
        self._dualsense_controller.connection_state.on_change(self._on_connection_change)

        # batt
        self._dualsense_controller.read_states.battery.on_change(lambda batt: print(f'battery: {batt}'))

        self._dualsense_controller.read_states.left_trigger_feedback.on_change(lambda fb: print(f'L2 TriggerFeedback: {fb}'))
        self._dualsense_controller.read_states.right_trigger_feedback.on_change(lambda fb: print(f'R2 TriggerFeedback: {fb}'))

        self._dualsense_controller.read_states.btn_ps.on_change(self._on_btn_ps)
        self._dualsense_controller.read_states.btn_options.on_change(self._on_btn_options)
        self._dualsense_controller.read_states.btn_create.on_change(self._on_btn_create)
        self._dualsense_controller.read_states.btn_mute.on_change(self._on_btn_mute)

        # 3 methods to get state changes of specific property
        self._dualsense_controller.on_state_change(ReadStateName.BTN_MUTE, self._on_btn_mute_1)
        self._dualsense_controller.read_states.on_change(ReadStateName.BTN_MUTE, self._on_btn_mute_2)
        self._dualsense_controller.read_states.btn_mute.on_change(self._on_btn_mute_3)

        self._dualsense_controller.read_states.btn_cross.on_change(self._on_btn_cross)
        self._dualsense_controller.read_states.btn_square.on_change(self._on_btn_square)
        self._dualsense_controller.read_states.btn_triangle.on_change(self._on_btn_triangle)
        self._dualsense_controller.read_states.btn_circle.on_change(self._on_btn_circle)

        self._dualsense_controller.read_states.btn_left.on_change(self._on_btn_left)
        self._dualsense_controller.read_states.btn_up.on_change(self._on_btn_up)
        self._dualsense_controller.read_states.btn_right.on_change(self._on_btn_right)
        self._dualsense_controller.read_states.btn_down.on_change(self._on_btn_down)

        self._dualsense_controller.read_states.btn_l1.on_change(self._on_btn_l1)
        self._dualsense_controller.read_states.btn_r1.on_change(self._on_btn_r1)
        self._dualsense_controller.read_states.btn_l3.on_change(self._on_btn_l3)
        self._dualsense_controller.read_states.btn_r3.on_change(self._on_btn_r3)

        self._dualsense_controller.read_states.left_trigger_value.on_change(self._on_l2)
        self._dualsense_controller.read_states.right_trigger_value.on_change(self._on_r2)

        # 4 methods to get all state changes
        self._dualsense_controller.on_any_state_change(self._on_any_state)
        self._dualsense_controller.read_states.on_any_change(self._on_any_state_3)
        self._dualsense_controller.on_state_change(self._on_any_state_2)
        self._dualsense_controller.read_states.on_change(self._on_any_state_4)

        # sticks
        self._dualsense_controller.read_states.left_stick_x.on_change(self._on_left_stick_x)
        self._dualsense_controller.read_states.left_stick_y.on_change(self._on_left_stick_y)
        self._dualsense_controller.read_states.left_stick.on_change(self._on_left_stick)

        self._dualsense_controller.read_states.right_stick_x.on_change(self._on_right_stick_x)
        self._dualsense_controller.read_states.right_stick_y.on_change(self._on_right_stick_y)
        self._dualsense_controller.read_states.right_stick.on_change(self._on_right_stick)

        # touch
        self._dualsense_controller.read_states.touch_finger_1.on_change(self._on_touch_finger_1)
        self._dualsense_controller.read_states.touch_finger_2.on_change(self._on_touch_finger_2)

        # other complex
        self._dualsense_controller.read_states.gyroscope.on_change(self._on_gyroscope)
        self._dualsense_controller.read_states.accelerometer.on_change(self._on_accelerometer)
        self._dualsense_controller.read_states.orientation.on_change(self._on_orientation)

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

    def _on_connection_change(self, state: Connection) -> None:
        print(f'Connection state changed. connected: {state.connected}, type: {state.connection_type}')

    def _on_btn_ps(self, state: bool) -> None:
        print(f'PS Button pressed: {state}')
        if state is False:  # if stop holding ps key
            self._stop()

    #
    # L1 / R1 -> brightness
    #
    def _on_btn_l1(self, state: bool) -> None:
        print(f'L1 Button pressed: {state} -> brightness ')
        self._dualsense_controller.set_state(
            WriteStateName.PLAYER_LEDS_BRIGHTNESS,
            PlayerLedsBrightness.LOW if state else PlayerLedsBrightness.HIGH
        )

    def _on_btn_r1(self, state: bool) -> None:
        print(f'R1 Button pressed: {state}')
        self._dualsense_controller.set_state(
            WriteStateName.PLAYER_LEDS_BRIGHTNESS,
            PlayerLedsBrightness.MEDIUM if state else PlayerLedsBrightness.HIGH
        )

    #
    # LEFT_TRIGGER / RIGHT_TRIGGER -> rumble
    #
    def _on_l2(self, value: int) -> None:
        print(f'L2 Analog Button: {value}')
        self._dualsense_controller.write_states.left_motor.value = value

    def _on_r2(self, value: int) -> None:
        print(f'R2 Analog Button: {value}')
        self._dualsense_controller.write_states.right_motor.value = value

    #
    # Left Controls -> lightbar color
    # Btn Create -> Lightbar off + Micro Mute
    #
    def _on_btn_left(self) -> None:
        print(f"lightbar red")
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 0)

    def _on_btn_up(self) -> None:
        print(f"lightbar green")
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 0)

    def _on_btn_right(self) -> None:
        print(f"lightbar blue")
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 0)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 255)

    def _on_btn_down(self) -> None:
        print(f"lightbar white")
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, 255)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, 255)

    def _on_btn_create(self, state: bool) -> None:
        print(f"lightbar false")
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_ON_OFF, state)
        self._dualsense_controller.set_state(WriteStateName.MICROPHONE_MUTE, state)

    #
    # Right Controls -> Player LED
    # Btn Options -> Player LED off + Micro LED
    #
    def _on_btn_square(self) -> None:
        print(f"player led center + outer")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LEDS_ENABLE, PlayerLedsEnable.CENTER | PlayerLedsEnable.OUTER)

    def _on_btn_triangle(self) -> None:
        print(f"player led inner")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LEDS_ENABLE, PlayerLedsEnable.INNER)

    def _on_btn_circle(self) -> None:
        print(f"player led outer")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LEDS_ENABLE, PlayerLedsEnable.OUTER)

    def _on_btn_cross(self, state: bool) -> None:
        if state:
            print(f"_on_btn_cross", self._dualsense_controller.read_states.btn_l1.value)
        print(f"player led all", state)
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LEDS_ENABLE, PlayerLedsEnable.ALL)

    def _on_btn_options(self, state: bool) -> None:
        print(f"player led off")
        self._dualsense_controller.set_state(WriteStateName.PLAYER_LEDS_ENABLE, PlayerLedsEnable.OFF)
        self._dualsense_controller.set_state(WriteStateName.MICROPHONE_LED, state)

    #
    # Microphone
    #
    def _on_btn_mute(self) -> None:
        print(f"mute")
        # self._dualsense_controller.set_state(WriteStateName.MICROPHONE_LED, state)
        # self._dualsense_controller.set_state(WriteStateName.MICROPHONE_MUTE, state)

    #
    # L3 / R3 -> led pulse modes
    #
    def _on_btn_r3(self, state: bool) -> None:
        if state is False:
            print(f"R3 -> pulse FADE_OUT")
            self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_PULSE_OPTIONS, LightbarPulseOptions.FADE_OUT_BLUE)

    def _on_btn_l3(self, state: bool) -> None:
        if state is False:
            print(f"L3 -> pulse FADE_BLUE")
            self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_PULSE_OPTIONS, LightbarPulseOptions.FADE_IN_BLUE)

    #
    # Touch0 x-value -> rgb-color
    #
    def _on_touch_finger_1(self, touch: TouchFinger) -> None:
        print('touch1', touch)
        x_max = 1920
        y_max = 1080
        x = min(x_max, max(0, touch.x))
        y = min(y_max, max(0, touch.y))

        color = int(0xffffff * x / x_max)
        red = (color >> 16) & 0xff
        green = (color >> 8) & 0xff
        blue = color & 0xff

        # print(f"Touch {x}-{y} -> color {hex(color)} {red}-{green}-{blue}")

        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_RED, red)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_GREEN, green)
        self._dualsense_controller.set_state(WriteStateName.LIGHTBAR_BLUE, blue)

    def _on_touch_finger_2(self, touch: TouchFinger) -> None:
        print('touch2', touch)

    #
    # all
    #
    def _on_any_state(self, name: ReadStateName, _: Any, state: Any, timestamp: int) -> None:
        # print(f'Any State {name}: {state} {timestamp}')
        pass

    def _on_any_state_2(self, name: ReadStateName, _: Any, state: Any, timestamp: int) -> None:
        # print(f'Any State 2 {name}: {state} {timestamp}')
        pass

    def _on_any_state_3(self, name: ReadStateName, _: Any, state: Any, timestamp: int) -> None:
        # print(f'Any State 3 {name}: {state} {timestamp}')
        pass

    def _on_any_state_4(self, name: ReadStateName, _: Any, state: Any, timestamp: int) -> None:
        # print(f'Any State 4 {name}: {state} {timestamp}')
        pass

    #
    # misc
    #
    def _on_btn_mute_1(self, state: bool) -> None:
        print(f'Mute Button pressed: {state}')
        if state:
            print(self._dualsense_controller.read_states.btn_mute.value)
            try:
                self._dualsense_controller.read_states.btn_mute.value = False
            except AttributeError:
                print('change the state from outside is not allowed.')
            print("batt lvl:", self._dualsense_controller.read_states.battery_level_percentage.value)
            print("batt is full:", self._dualsense_controller.read_states.battery_full.value)
            print("batt is charging", self._dualsense_controller.read_states.battery_charging.value)

    def _on_btn_mute_2(self, state: bool) -> None:
        print(f'Mute Button pressed 2: {state}')

    def _on_btn_mute_3(self, state: bool) -> None:
        print(f'Mute Button pressed 3: {state}')

    def _on_battery_low(self, percentage: float) -> None:
        print(f'Battery is low: {percentage}')

    #
    # STICKS
    #
    def _on_left_stick_x(self, state: int) -> None:
        print(f'Left JoyStick x: {state}')
        pass

    def _on_left_stick_y(self, state: int) -> None:
        print(f'Left JoyStick y: {state}')
        pass

    def _on_left_stick(self, state: JoyStick) -> None:
        print(f'Left JoyStick: {state}')
        pass

    def _on_right_stick(self, state: JoyStick) -> None:
        print(f'Right JoyStick: {state}')
        pass

    def _on_right_stick_x(self, state: int) -> None:
        print(f'Right JoyStick x: {state}')
        pass

    def _on_right_stick_y(self, state: int) -> None:
        print(f'Right JoyStick y: {state}')
        pass

    #
    # COMPLEX OTHER
    #
    def _on_gyroscope(self, state: Gyroscope) -> None:
        # print(f'Gyroscope: {state}')
        pass

    def _on_accelerometer(self, state: Accelerometer) -> None:
        # print(f'Accelerometer: {state}')
        pass

    def _on_orientation(self, state: Orientation) -> None:
        # print(f'Orientation: {state}')
        pass


def main():
    CoreExample().run()


if __name__ == "__main__":
    main()
