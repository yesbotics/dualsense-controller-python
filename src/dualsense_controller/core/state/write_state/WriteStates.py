from typing import Final

from dualsense_controller.core.report.out_report.OutReport import OutReport
from dualsense_controller.core.report.out_report.enum import OutBrightness, FlagsLights, OutFlagsPhysics, \
    OutLedOptions, OutPulseOptions, PlayerLeds
from dualsense_controller.core.state.BaseStates import BaseStates
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.ValueCompare import ValueCompare
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.mapping.typedef import MapFn
from dualsense_controller.core.state.typedef import CompareFn, StateChangeCallback, StateValue
from dualsense_controller.core.state.write_state.enum import WriteStateName
from dualsense_controller.core.state.write_state.value_type import Lightbar, Microphone


class WriteStates(BaseStates):

    def __init__(
            self,
            state_value_mapper: StateValueMapper,
    ):
        super().__init__(state_value_mapper)

        self._has_changed: bool = False

        # ################## MOTORS/RUMBLE
        self.left_motor: Final[State[int]] = self._create_and_register_state(
            WriteStateName.MOTOR_LEFT,
            value=0x00,
            mapped_to_raw_fn=self._state_value_mapper.set_left_motor_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.set_left_motor_raw_to_mapped,
        )
        self.right_motor: Final[State[int]] = self._create_and_register_state(
            WriteStateName.MOTOR_RIGHT,
            value=0x00,
            mapped_to_raw_fn=self._state_value_mapper.set_right_motor_mapped_to_raw,
            raw_to_mapped_fn=self._state_value_mapper.set_right_motor_raw_to_mapped,
        )

        # ################## LIGHTBAR
        self.lightbar: Final[State[Lightbar]] = self._create_and_register_state(
            WriteStateName.LIGHTBAR,
            value=Lightbar(0, 255, 0),
            compare_fn=ValueCompare.compare_lightbar,
            on_state_change_cb=self._on_lightbar_changed,
        )

        self.lightbar_red: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LIGHTBAR_RED,
            value=self.lightbar.value.red
        )
        self.lightbar_green: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LIGHTBAR_GREEN,
            value=self.lightbar.value.green
        )
        self.lightbar_blue: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LIGHTBAR_BLUE,
            value=self.lightbar.value.blue
        )
        self.lightbar_on_off = self._create_and_register_state(
            WriteStateName.LIGHTBAR_ON_OFF,
            value=self.lightbar.value.is_on
        )

        # ################## PLAYER LEDS
        self.player_leds: Final[State[PlayerLeds]] = self._create_and_register_state(
            name=WriteStateName.PLAYER_LEDS,
            value=PlayerLeds.OFF,
        )

        # ################## MICROPHONE
        self.microphone: Final[State[Microphone]] = self._create_and_register_state(
            name=WriteStateName.MICROPHONE,
            value=Microphone(),
            compare_fn=ValueCompare.compare_microphone,
            on_state_change_cb=self._on_microphone_changed,
            ignore_none=False,
        )
        self.microphone_mute: Final[State[bool]] = self._create_and_register_state(
            WriteStateName.MICROPHONE_MUTE,
            value=self.microphone.value.mute,
            ignore_none=False,
        )
        self.microphone_led: Final[State[bool]] = self._create_and_register_state(
            name=WriteStateName.MICROPHONE_LED,
            value=self.microphone.value.led,
            on_state_change_cb=self._on_microphone_led_changed,
            ignore_none=False,
        )

        # ################## FLAGS
        self._create_and_register_state(
            WriteStateName.FLAGS_PHYSICS,
            value=OutFlagsPhysics.ALL,
            disable_change_detection=True,
        )
        self._create_and_register_state(
            WriteStateName.FLAGS_LIGHTS,
            value=FlagsLights.ALL_BUT_MUTE_LED,
            disable_change_detection=True,
        )

        self._create_and_register_state(WriteStateName.L2_EFFECT_MODE, value=0x26)
        self._create_and_register_state(WriteStateName.L2_EFFECT_PARAM1, value=0x90)
        self._create_and_register_state(WriteStateName.L2_EFFECT_PARAM2, value=0xA0)
        self._create_and_register_state(WriteStateName.L2_EFFECT_PARAM3, value=0xFF)
        self._create_and_register_state(WriteStateName.L2_EFFECT_PARAM4, value=0x00)
        self._create_and_register_state(WriteStateName.L2_EFFECT_PARAM5, value=0x00)
        self._create_and_register_state(WriteStateName.L2_EFFECT_PARAM6, value=0x00)
        self._create_and_register_state(WriteStateName.L2_EFFECT_PARAM7, value=0x00)
        self._create_and_register_state(WriteStateName.R2_EFFECT_MODE, value=0x26)
        self._create_and_register_state(WriteStateName.R2_EFFECT_PARAM1, value=0x90)
        self._create_and_register_state(WriteStateName.R2_EFFECT_PARAM2, value=0xA0)
        self._create_and_register_state(WriteStateName.R2_EFFECT_PARAM3, value=0xFF)
        self._create_and_register_state(WriteStateName.R2_EFFECT_PARAM4, value=0x00)
        self._create_and_register_state(WriteStateName.R2_EFFECT_PARAM5, value=0x00)
        self._create_and_register_state(WriteStateName.R2_EFFECT_PARAM6, value=0x00)
        self._create_and_register_state(WriteStateName.R2_EFFECT_PARAM7, value=0x00)
        self._create_and_register_state(WriteStateName.LED_OPTIONS, value=OutLedOptions.ALL)
        self._create_and_register_state(WriteStateName.PULSE_OPTIONS, value=OutPulseOptions.FADE_OUT)
        self._create_and_register_state(WriteStateName.BRIGHTNESS, value=OutBrightness.HIGH)

    @property
    def has_changed(self) -> bool:
        return self._has_changed

    def set_value(self, name: WriteStateName, value: StateValue) -> None:
        state: State[StateValue] = self._get_state_by_name(name)
        state.value = value

    def set_value_without_triggering_change(self, name: WriteStateName, value: StateValue) -> None:
        state: State[StateValue] = self._get_state_by_name(name)
        state.set_value_without_triggering_change(value)

    def set_unchanged(self):
        self._get_state_by_name(WriteStateName.FLAGS_LIGHTS).set_value_without_triggering_change(
            FlagsLights.ALL_BUT_MUTE_LED
        )
        self._has_changed = False

    def update_out_report(self, out_report: OutReport):
        out_report.flags_physics = self._get_state_by_name(WriteStateName.FLAGS_PHYSICS).value_raw
        out_report.flags_lights = self._get_state_by_name(WriteStateName.FLAGS_LIGHTS).value_raw

        out_report.lightbar_red = self._get_state_by_name(WriteStateName.LIGHTBAR_RED).value_raw
        out_report.lightbar_green = self._get_state_by_name(WriteStateName.LIGHTBAR_GREEN).value_raw
        out_report.lightbar_blue = self._get_state_by_name(WriteStateName.LIGHTBAR_BLUE).value_raw
        out_report.motor_left = self._get_state_by_name(WriteStateName.MOTOR_LEFT).value_raw
        out_report.motor_right = self._get_state_by_name(WriteStateName.MOTOR_RIGHT).value_raw
        out_report.l2_effect_mode = self._get_state_by_name(WriteStateName.L2_EFFECT_MODE).value_raw
        out_report.l2_effect_param1 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM1).value_raw
        out_report.l2_effect_param2 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM2).value_raw
        out_report.l2_effect_param3 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM3).value_raw
        out_report.l2_effect_param4 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM4).value_raw
        out_report.l2_effect_param5 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM5).value_raw
        out_report.l2_effect_param6 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM6).value_raw
        out_report.l2_effect_param7 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM7).value_raw
        out_report.r2_effect_mode = self._get_state_by_name(WriteStateName.R2_EFFECT_MODE).value_raw
        out_report.r2_effect_param1 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM1).value_raw
        out_report.r2_effect_param2 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM2).value_raw
        out_report.r2_effect_param3 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM3).value_raw
        out_report.r2_effect_param4 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM4).value_raw
        out_report.r2_effect_param5 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM5).value_raw
        out_report.r2_effect_param6 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM6).value_raw
        out_report.r2_effect_param7 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM7).value_raw

        out_report.lightbar_on_off = self._get_state_by_name(WriteStateName.LIGHTBAR_ON_OFF).value_raw
        out_report.microphone_led = self._get_state_by_name(WriteStateName.MICROPHONE_LED).value_raw
        out_report.microphone_mute = self._get_state_by_name(WriteStateName.MICROPHONE_MUTE).value_raw
        out_report.led_options = self._get_state_by_name(WriteStateName.LED_OPTIONS).value_raw
        out_report.pulse_options = self._get_state_by_name(WriteStateName.PULSE_OPTIONS).value_raw
        out_report.brightness = self._get_state_by_name(WriteStateName.BRIGHTNESS).value_raw
        out_report.player_led = self._get_state_by_name(WriteStateName.PLAYER_LEDS).value_raw

    def _create_and_register_state(
            self,
            name: WriteStateName,
            value: StateValue = None,
            default_value: StateValue = None,
            on_state_change_cb: StateChangeCallback = None,
            mapped_to_raw_fn: MapFn = None,
            raw_to_mapped_fn: MapFn = None,
            ignore_none: bool = True,
            compare_fn: CompareFn = None,
            disable_change_detection: bool = False,
    ) -> State[StateValue]:
        state: State[StateValue] = State[StateValue](
            name=name,
            value=value,
            default_value=default_value,
            mapped_to_raw_fn=mapped_to_raw_fn,
            raw_to_mapped_fn=raw_to_mapped_fn,
            ignore_none=ignore_none,
            compare_fn=compare_fn,
            disable_change_detection=disable_change_detection,
        )
        self._register_state(name, state)
        state.on_change(on_state_change_cb if on_state_change_cb is not None else self._on_state_change)
        return state

    def _on_state_change(self):
        self._has_changed = True

    def _on_microphone_changed(self, mic: Microphone):
        self.microphone_mute.value = mic.mute
        self.microphone_led.value = mic.led
        self._has_changed = True

    def _on_lightbar_changed(self, lb: Lightbar):
        self.lightbar_red.value = lb.red
        self.lightbar_green.value = lb.green
        self.lightbar_blue.value = lb.blue
        self.lightbar_on_off.value = lb.is_on
        self._has_changed = True

    def _on_microphone_led_changed(self):
        # Remove mic control flag to allow setting brightness
        state: State[StateValue] = self._get_state_by_name(WriteStateName.FLAGS_LIGHTS)
        state.set_value_without_triggering_change(FlagsLights.ALL)
        self._has_changed = True
