from typing import Final

from dualsense_controller.api.property import AccelerometerProperty, BatteryProperty, BenchmarkProperty, ButtonProperty, \
    ConnectionProperty, \
    ExceptionProperty, \
    GyroscopeProperty, JoyStickProperty, \
    OrientationProperty, PlayerLedsProperty, RumbleProperty, \
    TouchFingerProperty, TriggerProperty
from dualsense_controller.core.Benchmarker import Benchmark
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.read_state.ReadStates import ReadStates
from dualsense_controller.core.state.read_state.value_type import Connection
from dualsense_controller.core.state.write_state.WriteStates import WriteStates


class Properties:
    def __init__(
            self,
            connection_state: State[Connection],
            update_benchmark_state: State[Benchmark],
            exception_state: State[Exception],
            read_states: ReadStates,
            write_states: WriteStates,
    ):
        # MAIN
        self.exceptions: Final[ExceptionProperty] = ExceptionProperty(exception_state)
        self.benchmark: Final[BenchmarkProperty] = BenchmarkProperty(update_benchmark_state)
        self.connection: Final[ConnectionProperty] = ConnectionProperty(connection_state)
        self.battery: Final[BatteryProperty] = BatteryProperty(read_states.battery)

        # BTN MISC
        self.btn_ps: Final[ButtonProperty] = ButtonProperty(read_states.btn_ps)
        self.btn_options: Final[ButtonProperty] = ButtonProperty(read_states.btn_options)
        self.btn_create: Final[ButtonProperty] = ButtonProperty(read_states.btn_create)
        self.btn_mute: Final[ButtonProperty] = ButtonProperty(read_states.btn_mute)
        self.btn_touchpad: Final[ButtonProperty] = ButtonProperty(read_states.btn_touchpad)

        # BTN SYMBOL
        self.btn_cross: Final[ButtonProperty] = ButtonProperty(read_states.btn_cross)
        self.btn_square: Final[ButtonProperty] = ButtonProperty(read_states.btn_square)
        self.btn_triangle: Final[ButtonProperty] = ButtonProperty(read_states.btn_triangle)
        self.btn_circle: Final[ButtonProperty] = ButtonProperty(read_states.btn_circle)

        # BTN DPAD
        self.btn_left: Final[ButtonProperty] = ButtonProperty(read_states.btn_left)
        self.btn_up: Final[ButtonProperty] = ButtonProperty(read_states.btn_up)
        self.btn_right: Final[ButtonProperty] = ButtonProperty(read_states.btn_right)
        self.btn_down: Final[ButtonProperty] = ButtonProperty(read_states.btn_down)

        # BTN L AND R
        self.btn_l1: Final[ButtonProperty] = ButtonProperty(read_states.btn_l1)
        self.btn_r1: Final[ButtonProperty] = ButtonProperty(read_states.btn_r1)
        self.btn_l2: Final[ButtonProperty] = ButtonProperty(read_states.btn_l2)
        self.btn_r2: Final[ButtonProperty] = ButtonProperty(read_states.btn_r2)
        self.btn_l3: Final[ButtonProperty] = ButtonProperty(read_states.btn_l3)
        self.btn_r3: Final[ButtonProperty] = ButtonProperty(read_states.btn_r3)

        # TRIGGERS
        self.left_trigger: Final[TriggerProperty] = TriggerProperty(read_states.left_trigger)
        self.right_trigger: Final[TriggerProperty] = TriggerProperty(read_states.right_trigger)

        # STICKS
        self.left_stick_x: Final[JoyStickProperty] = JoyStickProperty(read_states.left_stick_x)
        self.left_stick_y: Final[JoyStickProperty] = JoyStickProperty(read_states.left_stick_y)
        self.left_stick: Final[JoyStickProperty] = JoyStickProperty(read_states.left_stick)
        self.right_stick_x: Final[JoyStickProperty] = JoyStickProperty(read_states.right_stick_x)
        self.right_stick_y: Final[JoyStickProperty] = JoyStickProperty(read_states.right_stick_y)
        self.right_stick: Final[JoyStickProperty] = JoyStickProperty(read_states.right_stick)

        # TOUCH
        self.touch_finger_1: Final[TouchFingerProperty] = TouchFingerProperty(read_states.touch_finger_1)
        self.touch_finger_2: Final[TouchFingerProperty] = TouchFingerProperty(read_states.touch_finger_2)
        self.gyroscope: Final[GyroscopeProperty] = GyroscopeProperty(read_states.gyroscope)
        self.accelerometer: Final[AccelerometerProperty] = AccelerometerProperty(read_states.accelerometer)
        self.orientation: Final[OrientationProperty] = OrientationProperty(read_states.orientation)

        # WRITE
        self.left_rumble: Final[RumbleProperty] = RumbleProperty(write_states.left_motor)
        self.right_rumble: Final[RumbleProperty] = RumbleProperty(write_states.right_motor)
        self.player_leds: Final[PlayerLedsProperty] = PlayerLedsProperty(write_states.player_leds)

