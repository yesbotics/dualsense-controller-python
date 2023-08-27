from typing import Final

from dualsense_controller.core.report.out_report.OutReport import OutReport
from dualsense_controller.core.state.BaseStates import BaseStates
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.ValueCompare import ValueCompare
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.mapping.typedef import MapFn
from dualsense_controller.core.state.typedef import CompareFn, StateChangeCallback, StateValue
from dualsense_controller.core.state.write_state.enum import TriggerEffectMode, WriteStateName, LightbarPulseOptions, \
    PlayerLedsEnable, \
    FlagsPhysics, FlagsControls, LedOptions
from dualsense_controller.core.state.write_state.value_type import Lightbar, Microphone, PlayerLeds, \
    TriggerEffect


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
        self.lightbar_on_off: Final[State[bool]] = self._create_and_register_state(
            WriteStateName.LIGHTBAR_ON_OFF,
            value=self.lightbar.value.is_on
        )
        self.lightbar_pulse_options: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LIGHTBAR_PULSE_OPTIONS,
            value=LightbarPulseOptions.OFF
        )

        # ################## PLAYER LEDS
        self.player_leds: Final[State[PlayerLeds]] = self._create_and_register_state(
            name=WriteStateName.PLAYER_LEDS,
            compare_fn=ValueCompare.compare_player_leds,
            on_state_change_cb=self._on_player_leds_changed,
            value=PlayerLeds(),
        )
        self.player_leds_enable: Final[State[PlayerLedsEnable]] = self._create_and_register_state(
            name=WriteStateName.PLAYER_LEDS_ENABLE,
            value=self.player_leds.value.enable,
        )
        self.player_leds_brightness: Final[State[int]] = self._create_and_register_state(
            WriteStateName.PLAYER_LEDS_BRIGHTNESS,
            value=self.player_leds.value.brightness,
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
        self.flags_physics: Final[State[int]] = self._create_and_register_state(
            WriteStateName.FLAGS_PHYSICS,
            value=FlagsPhysics.ALL,
            disable_change_detection=True,
        )
        self.flags_controls: Final[State[int]] = self._create_and_register_state(
            WriteStateName.FLAGS_CONTROLS,
            value=FlagsControls.ALL_BUT_MUTE_LED,
            disable_change_detection=True,
        )
        self.led_options: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LED_OPTIONS,
            value=LedOptions.ALL
        )

        # ################## LEFT TRIGGER
        self.left_trigger_effect: Final[State[TriggerEffect]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT,
            value=TriggerEffect(),
            compare_fn=ValueCompare.compare_trigger_effect,
            on_state_change_cb=self._on_left_trigger_effect_changed,
        )
        self.left_trigger_effect_mode: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_MODE,
            value=TriggerEffectMode.NO_RESISTANCE
        )
        self.left_trigger_effect_param1: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM1,
            value=0x00
        )
        self.left_trigger_effect_param2: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM2,
            value=0x00
        )
        self.left_trigger_effect_param3: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM3,
            value=0x00
        )
        self.left_trigger_effect_param4: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM4,
            value=0x00
        )
        self.left_trigger_effect_param5: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM5,
            value=0x00
        )
        self.left_trigger_effect_param6: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM6,
            value=0x00
        )
        self.left_trigger_effect_param7: Final[State[int]] = self._create_and_register_state(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM7,
            value=0x00
        )

        # ################## RIGHT TRIGGER
        self.right_trigger_effect: Final[State[TriggerEffect]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT,
            value=TriggerEffect(),
            compare_fn=ValueCompare.compare_trigger_effect,
            on_state_change_cb=self._on_right_trigger_effect_changed,
        )
        self.right_trigger_effect_mode: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_MODE,
            value=TriggerEffectMode.NO_RESISTANCE
        )
        self.right_trigger_effect_param1: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM1,
            value=0x00
        )
        self.right_trigger_effect_param2: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM2,
            value=0x00
        )
        self.right_trigger_effect_param3: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM3,
            value=0x00
        )
        self.right_trigger_effect_param4: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM4,
            value=0x00
        )
        self.right_trigger_effect_param5: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM5,
            value=0x00
        )
        self.right_trigger_effect_param6: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM6,
            value=0x00
        )
        self.right_trigger_effect_param7: Final[State[int]] = self._create_and_register_state(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM7,
            value=0x00
        )

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
        self._get_state_by_name(WriteStateName.FLAGS_CONTROLS).set_value_without_triggering_change(
            FlagsControls.ALL_BUT_MUTE_LED
        )
        self._has_changed = False

    def update_out_report(self, out_report: OutReport):
        out_report.flags_physics = self.flags_physics.value_raw
        out_report.flags_controls = self.flags_controls.value_raw

        out_report.lightbar_red = self.lightbar_red.value_raw
        out_report.lightbar_green = self.lightbar_green.value_raw
        out_report.lightbar_blue = self.lightbar_blue.value_raw
        out_report.lightbar_on_off = self.lightbar_on_off.value_raw
        out_report.lightbar_pulse_options = self.lightbar_pulse_options.value_raw

        out_report.motor_left = self.left_motor.value_raw
        out_report.motor_right = self.right_motor.value_raw

        out_report.microphone_led = self.microphone_led.value_raw
        out_report.microphone_mute = self.microphone_mute.value_raw

        out_report.led_options = self.led_options.value_raw

        out_report.player_leds_enable = self.player_leds_enable.value_raw
        out_report.player_leds_brightness = self.player_leds_brightness.value_raw

        out_report.left_trigger_effect_mode = self._get_state_by_name(WriteStateName.LEFT_TRIGGER_EFFECT_MODE).value_raw
        out_report.left_trigger_effect_param1 = self._get_state_by_name(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM1).value_raw
        out_report.left_trigger_effect_param2 = self._get_state_by_name(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM2).value_raw
        out_report.left_trigger_effect_param3 = self._get_state_by_name(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM3).value_raw
        out_report.left_trigger_effect_param4 = self._get_state_by_name(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM4).value_raw
        out_report.left_trigger_effect_param5 = self._get_state_by_name(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM5).value_raw
        out_report.left_trigger_effect_param6 = self._get_state_by_name(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM6).value_raw
        out_report.left_trigger_effect_param7 = self._get_state_by_name(
            WriteStateName.LEFT_TRIGGER_EFFECT_PARAM7).value_raw
        out_report.right_trigger_effect_mode = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_MODE).value_raw
        out_report.right_trigger_effect_param1 = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM1).value_raw
        out_report.right_trigger_effect_param2 = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM2).value_raw
        out_report.right_trigger_effect_param3 = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM3).value_raw
        out_report.right_trigger_effect_param4 = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM4).value_raw
        out_report.right_trigger_effect_param5 = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM5).value_raw
        out_report.right_trigger_effect_param6 = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM6).value_raw
        out_report.right_trigger_effect_param7 = self._get_state_by_name(
            WriteStateName.RIGHT_TRIGGER_EFFECT_PARAM7).value_raw

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

    def _on_state_change(self) -> None:
        self._has_changed = True

    def _on_microphone_changed(self, mic: Microphone) -> None:
        self.microphone_mute.value = mic.mute
        self.microphone_led.value = mic.led
        self._has_changed = True

    def _on_player_leds_changed(self, leds: PlayerLeds) -> None:
        self.player_leds_enable.value = leds.enable
        self.player_leds_brightness.value = leds.brightness
        self._has_changed = True

    def _on_lightbar_changed(self, lb: Lightbar) -> None:
        self.lightbar_red.value = lb.red
        self.lightbar_green.value = lb.green
        self.lightbar_blue.value = lb.blue
        self.lightbar_on_off.value = lb.is_on
        self.lightbar_pulse_options.value = lb.pulse_options
        self._has_changed = True

    def _on_microphone_led_changed(self) -> None:
        # Remove mic control flag to allow setting brightness
        self.flags_controls.set_value_without_triggering_change(FlagsControls.ALL)
        self._has_changed = True

    def _on_left_trigger_effect_changed(self, left_trigger_effect: TriggerEffect) -> None:
        print('_on_left_trigger_effect_changed', left_trigger_effect)
        self.left_trigger_effect_mode.value = left_trigger_effect.mode
        self.left_trigger_effect_param1.value = left_trigger_effect.param1
        self.left_trigger_effect_param2.value = left_trigger_effect.param2
        self.left_trigger_effect_param3.value = left_trigger_effect.param3
        self.left_trigger_effect_param4.value = left_trigger_effect.param4
        self.left_trigger_effect_param5.value = left_trigger_effect.param5
        self.left_trigger_effect_param6.value = left_trigger_effect.param6
        self.left_trigger_effect_param7.value = left_trigger_effect.param7
        self._has_changed = True

    def _on_right_trigger_effect_changed(self, right_trigger_effect: TriggerEffect) -> None:
        print('_on_right_trigger_effect_changed', right_trigger_effect)
        self.right_trigger_effect_mode.value = right_trigger_effect.mode
        self.right_trigger_effect_param1.value = right_trigger_effect.param1
        self.right_trigger_effect_param2.value = right_trigger_effect.param2
        self.right_trigger_effect_param3.value = right_trigger_effect.param3
        self.right_trigger_effect_param4.value = right_trigger_effect.param4
        self.right_trigger_effect_param5.value = right_trigger_effect.param5
        self.right_trigger_effect_param6.value = right_trigger_effect.param6
        self.right_trigger_effect_param7.value = right_trigger_effect.param7
        self._has_changed = True
