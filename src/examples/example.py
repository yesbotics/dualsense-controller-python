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


class Example:

    def __init__(self):
        self.is_running: bool = True
        device_infos: list[DeviceInfo] = DualSenseController.enumerate_devices()
        if len(device_infos) < 1:
            raise Exception('No DualSense Controller available.')
        first_device_info: DeviceInfo = device_infos[0]
        self.controller: DualSenseController = DualSenseController(

            device_index_or_device_info=first_device_info,

            # mapping=Mapping.NORMALIZED,
            # left_joystick_deadzone=0.2,
            # right_joystick_deadzone=0.2,
            # left_trigger_deadzone=0.05,
            # right_trigger_deadzone=0.05,

            mapping=Mapping.RAW,
            left_joystick_deadzone=5,
            right_joystick_deadzone=5,
            left_trigger_deadzone=1,
            right_trigger_deadzone=1,

            gyroscope_threshold=0,
            accelerometer_threshold=0,
            orientation_threshold=0,

            # update_level=UpdateLevel.PAINSTAKING,
            # update_level=UpdateLevel.HAENGBLIEM,
            update_level=UpdateLevel.DEFAULT,

            microphone_initially_muted=True,
            microphone_invert_led=False,
        )

        # MAIN
        self.controller.exceptions.on_change(self.on_exception)
        self.controller.benchmark.on_change(self.on_benchmark)

        self.controller.connection.on_change(self.on_connection_change)
        self.controller.connection.on_connected(self.on_connection_connected)
        self.controller.connection.on_disconnected(self.on_connection_disconnected)

        self.controller.battery.on_change(self.on_battery_change)
        self.controller.battery.on_lower_than(75, self.on_battery_lower_than)
        self.controller.battery.on_charging(self.on_battery_charging)
        self.controller.battery.on_discharging(self.on_battery_discharging)

        # BTN MISC
        self.controller.btn_ps.on_down(self.on_btn_ps_down)
        self.controller.btn_options.on_down(self.on_btn_options_down)
        self.controller.btn_create.on_down(self.on_btn_create_down)
        self.controller.btn_mute.on_down(self.on_btn_mute_down)
        self.controller.btn_touchpad.on_down(self.on_btn_touchpad_down)

        # BTN SYMBOL
        self.controller.btn_triangle.on_up(self.on_btn_triangle_up)
        self.controller.btn_triangle.on_down(self.on_btn_triangle_down)
        self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_1)
        self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_2)
        self.controller.btn_triangle.on_change(self.on_btn_triangle_changed_3)
        self.controller.btn_cross.on_down(self.on_btn_cross_down)
        self.controller.btn_circle.on_down(self.on_btn_circle_down)
        self.controller.btn_square.on_down(self.on_btn_square_down)

        # BTN DPAD
        self.controller.btn_left.on_down(self.on_btn_left_down)
        self.controller.btn_up.on_down(self.on_btn_up_down)
        self.controller.btn_right.on_down(self.on_btn_right_down)
        self.controller.btn_down.on_down(self.on_btn_down_down)

        # BTN L and R
        self.controller.btn_l1.on_change(self.on_btn_l1_changed)
        self.controller.btn_r1.on_down(self.on_btn_r1_down)
        self.controller.btn_l2.on_down(self.on_btn_l2_down)
        self.controller.btn_r2.on_down(self.on_btn_r2_down)
        self.controller.btn_r3.on_down(self.on_btn_r3_down)
        self.controller.btn_l3.on_down(self.on_btn_l3_down)

        # TRIGGERS
        self.controller.left_trigger.on_change(self.on_left_trigger_changed)
        self.controller.right_trigger.on_change(self.on_right_trigger_changed)

        # STICKS
        self.controller.left_stick_x.on_change(self.on_left_stick_x_changed)
        self.controller.left_stick_y.on_change(self.on_left_stick_y_changed)
        self.controller.left_stick.on_change(self.on_left_stick_changed)
        self.controller.right_stick_x.on_change(self.on_right_stick_x_changed)
        self.controller.right_stick_y.on_change(self.on_right_stick_y_changed)
        self.controller.right_stick.on_change(self.on_right_stick_changed)

        # TOUCH
        self.controller.touch_finger_1.on_change(self.on_touch_finger_1_change)
        self.controller.touch_finger_2.on_change(self.on_touch_finger_2_change)

        # IMU
        self.controller.gyroscope.on_change(self.on_gyroscope_change)
        self.controller.accelerometer.on_change(self.on_accelerometer_change)
        self.controller.orientation.on_change(self.on_orientation_change)

    def run(self) -> None:
        self.controller.activate()
        while self.is_running:
            time.sleep(1)
        self.controller.deactivate()

    # ############################################# MAIN ##################################################
    def on_exception(self, exception: Exception) -> None:
        print(f'Exception occured:', exception)
        self.is_running = False

    def on_benchmark(self, benchmark_result: Benchmark) -> None:
        # print(f'Benchmark: {benchmark_result}')
        pass

    def on_connection_change(self, connection: Connection) -> None:
        print(f'on connection change: {connection}')

    def on_connection_connected(self, connection_type: ConnectionType) -> None:
        print(f'on connection connect: {connection_type}')

    def on_connection_disconnected(self, connection_type: ConnectionType) -> None:
        print(f'on connection disconnect: {connection_type}')

    def on_battery_change(self, battery: Battery) -> None:
        print(f'on battery change: {battery}')

    def on_battery_lower_than(self, battery_level) -> None:
        print(f'on battery low: {battery_level}')

    def on_battery_charging(self, battery_level) -> None:
        print(f'on battery charging: {battery_level}')

    def on_battery_discharging(self, battery_level) -> None:
        print(f'on battery discharging: {battery_level}')

    # ############################################# BTN MISC ##################################################
    def on_btn_ps_down(self) -> None:
        print(f'PS button down -> stop')
        self.is_running = False

    def on_btn_options_down(self) -> None:
        print(f"on_btn_options_down -> player led off")
        self.controller.player_leds.set_off()

    # Btn Create -> Lightbar off
    def on_btn_create_down(self) -> None:
        print(f"on_btn_create_down -> lightbar toggle")
        warnings.warn("toggle lightbar not working properly -> check it!", UserWarning)
        self.controller.lightbar.toggle_on_off()

    def on_btn_mute_down(self) -> None:
        print(f"mute")
        print(f'Mute Button pressed')
        print("batt lvl:", self.controller.battery.value.level_percentage)
        print("batt is full:", self.controller.battery.value.full)
        print("batt is charging", self.controller.battery.value.charging)
        self.controller.microphone.toggle_muted()
        print('self.controller.microphone, muted:', self.controller.microphone.is_muted)

    def on_btn_touchpad_down(self) -> None:
        print(f"on_btn_touchpad_down")

    # ########################################### BTN DPAD -> LIGHTBAR COLOR ####################################

    def on_btn_left_down(self) -> None:
        print(f"btn_left_down -> lightbar red, left trigger section resistance")
        self.controller.lightbar.set_color_red()
        self.controller.left_trigger.effect.set_section_resistance()

    def on_btn_up_down(self) -> None:
        print(f"btn_up_down -> lightbar green, left trigger continuous resistance")
        self.controller.lightbar.set_color_green()
        self.controller.left_trigger.effect.set_continuous_resistance()

    def on_btn_right_down(self) -> None:
        print(f"btn_right_down -> lightbar blue, left trigger effect ext")
        self.controller.lightbar.set_color_blue()
        self.controller.left_trigger.effect.set_effect_extended()

    def on_btn_down_down(self) -> None:
        print(f"btn_down_down -> lightbar white, left trigger vibrating")
        self.controller.lightbar.set_color_white()
        self.controller.left_trigger.effect.set_vibrating()

    # ########################################### BTN SYMBOL -> PLAYED LED ####################################

    def on_btn_triangle_up(self) -> None:
        print(f'Triangle button -> up')

    def on_btn_triangle_changed_1(self, pressed: bool) -> None:
        print(f'Triangle button: pressed: {pressed}')

    def on_btn_triangle_changed_2(self, pressed: bool, timestamp: int) -> None:
        print(f'Triangle button: pressed: {pressed}, timestamp: {timestamp}')

    def on_btn_triangle_changed_3(self, last_pressed: bool, pressed: bool, timestamp: int) -> None:
        print(f'Triangle button: last_pressed: {last_pressed}, pressed: {pressed}, timestamp: {timestamp}')

    def on_btn_triangle_down(self) -> None:
        print(f'Triangle button down -> player led inner, right trigger section resistance')
        self.controller.player_leds.set_inner()
        self.controller.right_trigger.effect.set_continuous_resistance()

    def on_btn_cross_down(self) -> None:
        print(f'Cross button down -> player led all, right trigger vibrating')
        self.controller.player_leds.set_all()
        self.controller.right_trigger.effect.set_vibrating()

    def on_btn_circle_down(self) -> None:
        print(f'btn circle down -> player led outer, right trigger effect ext')
        self.controller.player_leds.set_outer()
        self.controller.right_trigger.effect.set_effect_extended()

    def on_btn_square_down(self) -> None:
        print(f'btn square down -> player led center + outer, right trigger section resistance')
        self.controller.player_leds.set_center_and_outer()
        self.controller.right_trigger.effect.set_section_resistance()

    # ################################ BTN L and R -> brightness, nothing and led pulse modes ####################
    def on_btn_l1_changed(self, pressed: bool) -> None:
        print(f'L1 Button pressed: {pressed} -> brightness, left trigger no resistance')
        if pressed:
            self.controller.player_leds.set_brightness_high()
            self.controller.left_trigger.effect.set_no_resistance()
        else:
            self.controller.player_leds.set_brightness_low()

    def on_btn_r1_down(self) -> None:
        print(f'R1 Button pressed: -> brightness medium, right trigger no resistance')
        self.controller.player_leds.set_brightness_medium()
        self.controller.right_trigger.effect.set_no_resistance()

    def on_btn_l2_down(self) -> None:
        print(f'on_btn_l2_down -> ')

    def on_btn_r2_down(self) -> None:
        print(f'on_btn_r3_down -> ')

    def on_btn_l3_down(self) -> None:
        print(f'L3 -> pulse FADE_BLUE')
        self.controller.lightbar.fade_in_blue()

    def on_btn_r3_down(self) -> None:
        print(f'R3 -> pulse FADE_OUT')
        self.controller.lightbar.fade_out_blue()

    # ########################################### TRIGGERS -> RUMBLE ##############################################
    def on_left_trigger_changed(self, value: Number) -> None:
        if self.controller.microphone.is_muted:
            print(f'L2 trigger: {value}')
            self.controller.left_rumble.set(value)
            print(f'Left Rumble: {self.controller.left_rumble.value}')

    def on_right_trigger_changed(self, value: Number) -> None:
        if self.controller.microphone.is_muted:
            print(f'L2 trigger: {value}')
            self.controller.right_rumble.set(value)
            print(f'Right Rumble: {self.controller.right_rumble.value}')

    # ############################################# STICKS ##################################################

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

    # ############################################# TOUCH ##################################################

    def on_touch_finger_1_change(self, touch_finger_1: TouchFinger):
        print(f'on_touch_finger_1_change: {touch_finger_1} -> rgb-color')
        x_max = 1920
        y_max = 1080
        x = min(x_max, max(0, touch_finger_1.x))
        y = min(y_max, max(0, touch_finger_1.y))
        color = int(0xffffff * x / x_max)
        red = (color >> 16) & 0xff
        green = (color >> 8) & 0xff
        blue = color & 0xff
        # print(f"Touch {x}-{y} -> color {hex(color)} {red}-{green}-{blue}")
        self.controller.lightbar.set_color(red, green, blue)

    def on_touch_finger_2_change(self, touch_finger_1: TouchFinger):
        print(f'on_touch_finger_2_change -> {touch_finger_1}')

    # ############################################# IMU ##################################################

    def on_gyroscope_change(self, gyroscope: Gyroscope):
        # print(f'on_gyroscope_change: {gyroscope} -> ')
        pass

    def on_accelerometer_change(self, accelerometer: Accelerometer):
        # print(f'on_accelerometer_change: {accelerometer} -> ')
        pass

    def on_orientation_change(self, orientation: Orientation):
        # print(f'on_orientation_change: {orientation} -> ')
        pass


# ############################################# RUN EXAMPLE ##################################################

def main():
    Example().run()


if __name__ == "__main__":
    main()
