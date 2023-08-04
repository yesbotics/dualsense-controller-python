from typing import Final

from dualsense_controller.report.out_report.OutReport import OutReport
from dualsense_controller.report.out_report.enum import OutBrightness, OutFlagsLights, OutFlagsPhysics, OutLedOptions, \
    OutPulseOptions
from dualsense_controller.state.State import State
from dualsense_controller.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.state.mapping.typedef import MapFn
from dualsense_controller.state.typedef import StateChangeCallback, StateValueType
from dualsense_controller.state.write_state.enum import WriteStateName


class WriteStates:

    def __init__(
            self,
            state_value_mapper: StateValueMapper,
    ):

        self._states_dict: Final[dict[WriteStateName, State]] = {}
        self._state_value_mapper: Final[StateValueMapper] = state_value_mapper

        self._changed = False

        self._create_and_register_state(WriteStateName.FLAGS_PHYSICS, value=OutFlagsPhysics.ALL)
        self._create_and_register_state(WriteStateName.FLAGS_LIGHTS, value=OutFlagsLights.ALL_BUT_MUTE_LED)

        self._create_and_register_state(WriteStateName.LIGHTBAR_RED, value=0xff)
        self._create_and_register_state(WriteStateName.LIGHTBAR_GREEN, value=0xff)
        self._create_and_register_state(WriteStateName.LIGHTBAR_BLUE, value=0xff)
        self._create_and_register_state(
            WriteStateName.MOTOR_LEFT,
            value=0x00,
            mapped_to_raw_fn=self._state_value_mapper.set_left_motor_mapped_to_raw
        )
        self._create_and_register_state(
            WriteStateName.MOTOR_RIGHT,
            value=0x00,
            mapped_to_raw_fn=self._state_value_mapper.set_right_motor_mapped_to_raw
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

        self._create_and_register_state(WriteStateName.LIGHTBAR, value=True)
        self._create_and_register_state(WriteStateName.MICROPHONE_LED, value=False, callback=self._on_change_mute_led)
        self._create_and_register_state(WriteStateName.MICROPHONE_MUTE, value=True)
        self._create_and_register_state(WriteStateName.LED_OPTIONS, value=OutLedOptions.ALL)
        self._create_and_register_state(WriteStateName.PULSE_OPTIONS, value=OutPulseOptions.FADE_OUT)
        self._create_and_register_state(WriteStateName.BRIGHTNESS, value=OutBrightness.HIGH)
        self._create_and_register_state(WriteStateName.PLAYER_LED, value=0x00)

    @property
    def changed(self) -> bool:
        return self._changed

    def set_value(self, name: WriteStateName, value: StateValueType, trigger_change: bool = True) -> None:
        state: State[StateValueType] = self._get_state_by_name(name)
        if not trigger_change:
            state.set_value_without_triggering_change(value)
        else:
            state.set_value(value)

    def set_value_mapped(self, name: WriteStateName, value: StateValueType, trigger_change: bool = True) -> None:
        state: State[StateValueType] = self._get_state_by_name(name)
        if not trigger_change:
            state.set_value_mapped_without_triggering_change(value)
        else:
            state.set_value_mapped(value)

    def set_unchanged(self):
        self._get_state_by_name(WriteStateName.FLAGS_LIGHTS).set_value_without_triggering_change(
            OutFlagsLights.ALL_BUT_MUTE_LED
        )
        self._changed = False

    def update_out_report(self, out_report: OutReport):
        out_report.flags_physics = self._get_state_by_name(WriteStateName.FLAGS_PHYSICS).value
        out_report.flags_lights = self._get_state_by_name(WriteStateName.FLAGS_LIGHTS).value

        out_report.lightbar_red = self._get_state_by_name(WriteStateName.LIGHTBAR_RED).value
        out_report.lightbar_green = self._get_state_by_name(WriteStateName.LIGHTBAR_GREEN).value
        out_report.lightbar_blue = self._get_state_by_name(WriteStateName.LIGHTBAR_BLUE).value
        out_report.motor_left = self._get_state_by_name(WriteStateName.MOTOR_LEFT).value
        out_report.motor_right = self._get_state_by_name(WriteStateName.MOTOR_RIGHT).value
        out_report.l2_effect_mode = self._get_state_by_name(WriteStateName.L2_EFFECT_MODE).value
        out_report.l2_effect_param1 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM1).value
        out_report.l2_effect_param2 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM2).value
        out_report.l2_effect_param3 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM3).value
        out_report.l2_effect_param4 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM4).value
        out_report.l2_effect_param5 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM5).value
        out_report.l2_effect_param6 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM6).value
        out_report.l2_effect_param7 = self._get_state_by_name(WriteStateName.L2_EFFECT_PARAM7).value
        out_report.r2_effect_mode = self._get_state_by_name(WriteStateName.R2_EFFECT_MODE).value
        out_report.r2_effect_param1 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM1).value
        out_report.r2_effect_param2 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM2).value
        out_report.r2_effect_param3 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM3).value
        out_report.r2_effect_param4 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM4).value
        out_report.r2_effect_param5 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM5).value
        out_report.r2_effect_param6 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM6).value
        out_report.r2_effect_param7 = self._get_state_by_name(WriteStateName.R2_EFFECT_PARAM7).value

        out_report.lightbar = self._get_state_by_name(WriteStateName.LIGHTBAR.LIGHTBAR).value
        out_report.microphone_led = self._get_state_by_name(WriteStateName.MICROPHONE_LED).value
        out_report.microphone_mute = self._get_state_by_name(WriteStateName.MICROPHONE_MUTE).value
        out_report.led_options = self._get_state_by_name(WriteStateName.LED_OPTIONS).value
        out_report.pulse_options = self._get_state_by_name(WriteStateName.PULSE_OPTIONS).value
        out_report.brightness = self._get_state_by_name(WriteStateName.BRIGHTNESS).value
        out_report.player_led = self._get_state_by_name(WriteStateName.PLAYER_LED).value

    def _get_state_by_name(self, name: WriteStateName) -> State:
        return self._states_dict[name]

    def _create_and_register_state(
            self,
            name: WriteStateName,
            value: StateValueType = None,
            callback: StateChangeCallback = None,
            mapped_to_raw_fn: MapFn = None,
    ) -> State[StateValueType]:
        if callback is None:
            callback = self._on_change
        state: State[StateValueType] = State[StateValueType](
            name=name,
            value=value,
            mapped_to_raw_fn=mapped_to_raw_fn
        )
        state.on_change(callback)
        return state

    def _on_change(self, _, __):
        self._changed = True

    def _on_change_mute_led(self):
        # Remove mic control flag to allow setting brightness
        self.set_value(WriteStateName.FLAGS_LIGHTS, OutFlagsLights.ALL, False)
        self._changed = True
