from dualsense_controller.common import (
    OutLedOptions,
    OutPulseOptions,
    OutBrightness,
    OutFlagsLights,
    OutFlagsPhysics,
)
from dualsense_controller.report import OutReport
from dualsense_controller.state import BaseStates, StateValueType, StateChangeCallback, WriteStateName


class WriteStates(BaseStates[WriteStateName]):

    def __init__(
            self,
    ):
        super().__init__()

        self._changed = False

        self._create_state(WriteStateName.FLAGS_PHYSICS, OutFlagsPhysics.ALL)
        self._create_state(WriteStateName.FLAGS_LIGHTS, OutFlagsLights.ALL_BUT_MUTE_LED)

        self._create_state(WriteStateName.LIGHTBAR_RED, 0xff)
        self._create_state(WriteStateName.LIGHTBAR_GREEN, 0xff)
        self._create_state(WriteStateName.LIGHTBAR_BLUE, 0xff)
        self._create_state(WriteStateName.MOTOR_LEFT, 0x00)
        self._create_state(WriteStateName.MOTOR_RIGHT, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_MODE, 0x26)
        self._create_state(WriteStateName.L2_EFFECT_PARAM1, 0x90)
        self._create_state(WriteStateName.L2_EFFECT_PARAM2, 0xA0)
        self._create_state(WriteStateName.L2_EFFECT_PARAM3, 0xFF)
        self._create_state(WriteStateName.L2_EFFECT_PARAM4, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_PARAM5, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_PARAM6, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_PARAM7, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_MODE, 0x26)
        self._create_state(WriteStateName.R2_EFFECT_PARAM1, 0x90)
        self._create_state(WriteStateName.R2_EFFECT_PARAM2, 0xA0)
        self._create_state(WriteStateName.R2_EFFECT_PARAM3, 0xFF)
        self._create_state(WriteStateName.R2_EFFECT_PARAM4, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_PARAM5, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_PARAM6, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_PARAM7, 0x00)

        self._create_state(WriteStateName.LIGHTBAR, True)
        self._create_state(WriteStateName.MICROPHONE_LED, False, self._on_change_mute_led)
        self._create_state(WriteStateName.MICROPHONE_MUTE, True)
        self._create_state(WriteStateName.LED_OPTIONS, OutLedOptions.ALL)
        self._create_state(WriteStateName.PULSE_OPTIONS, OutPulseOptions.FADE_OUT)
        self._create_state(WriteStateName.BRIGHTNESS, OutBrightness.HIGH)
        self._create_state(WriteStateName.PLAYER_LED, 0x00)

    @property
    def changed(self) -> bool:
        return self._changed

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

    def _create_state(
            self,
            name: WriteStateName,
            value: StateValueType = None,
            callback: StateChangeCallback = None
    ) -> None:
        if callback is None:
            callback = self._on_change
        self._create_and_register_state(name, value).on_change(callback)

    def _on_change(self, _, __):
        self._changed = True

    def _on_change_mute_led(self, _, __):
        # Remove mic control flag to allow setting brightness
        self.set_value(WriteStateName.FLAGS_LIGHTS, OutFlagsLights.ALL, False)
        self._changed = True
