from dualsense_controller.core.report.out_report.OutReport import OutReport
from dualsense_controller.core.report.out_report.enum import OutReportLength
from dualsense_controller.core.report.out_report.util import clamp_byte
from dualsense_controller.core.state.write_state.enum import LightbarMode


class Usb01OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> usb")

        # reportId = 0x02

        out_report_bytes: bytearray = bytearray(OutReportLength.USB_01)

        # report type
        out_report_bytes[0] = self.operating_mode

        # report data
        out_report_bytes[1] = self.flags_physics

        #
        # valid_flag1 - further flags determining what changes this packet will perform
        # or: LightEffectMode
        #
        # bit 0: MIC_MUTE_LED_CONTROL_ENABLE - toggling microphone LED
        # bit 1: POWER_SAVE_CONTROL_ENABLE - toggling audio/mic mute
        # bit 2: LIGHTBAR_CONTROL_ENABLE - toggling LED strips on the sides of the touchpad
        # bit 3: RELEASE_LEDS - will actively turn all LEDs off? Convenience flag?
        # bit 4: PLAYER_INDICATOR_CONTROL_ENABLE - toggling white player indicator LEDs below touchpad
        # bit 5: ???
        # bit 6: adjustment of overall motor/effect power (index 37 - read note on triggers)
        # bit 7: ???
        out_report_bytes[2] = self.flags_controls

        # DualShock 4 compatibility update_level.
        out_report_bytes[3] = clamp_byte(self.motor_right)
        out_report_bytes[4] = clamp_byte(self.motor_left)

        # mute_button_led
        # 0: mute LED off
        # 1: mute LED on
        out_report_bytes[9] = self.microphone_led

        # power_save_control
        # bit 4: POWER_SAVE_CONTROL_MIC_MUTE
        out_report_bytes[10] = 0x10 if self.microphone_mute else 0x00

        # Right trigger effect
        # UpdateLevel
        # 0x00: off
        # 0x01: mode1
        # 0x02: mode2
        # 0x05: mode1 + mode4
        # 0x06: mode2 + mode4
        # 0x21: mode1 + mode20
        # 0x25: mode1 + mode4 + mode20
        # 0x26: mode2 + mode4 + mode20
        # 0xFC: calibration
        out_report_bytes[11] = self.right_trigger_effect_mode
        out_report_bytes[12] = self.right_trigger_effect_param1
        out_report_bytes[13] = self.right_trigger_effect_param2
        out_report_bytes[14] = self.right_trigger_effect_param3
        out_report_bytes[15] = self.right_trigger_effect_param4
        out_report_bytes[16] = self.right_trigger_effect_param5
        out_report_bytes[17] = self.right_trigger_effect_param6
        out_report_bytes[20] = self.right_trigger_effect_param7

        out_report_bytes[22] = self.left_trigger_effect_mode
        out_report_bytes[23] = self.left_trigger_effect_param1
        out_report_bytes[24] = self.left_trigger_effect_param2
        out_report_bytes[25] = self.left_trigger_effect_param3
        out_report_bytes[26] = self.left_trigger_effect_param4
        out_report_bytes[27] = self.left_trigger_effect_param5
        out_report_bytes[28] = self.left_trigger_effect_param6
        out_report_bytes[31] = self.left_trigger_effect_param7

        out_report_bytes[39] = self.led_options

        # Lightbar on/off
        out_report_bytes[41] = LightbarMode.LIGHT_ON if self.lightbar_on_off else LightbarMode.LIGHT_OFF

        # Disable/Endable LEDs or Pulse/Fade-Options?
        out_report_bytes[42] = self.lightbar_pulse_options
        out_report_bytes[43] = self.player_leds_brightness
        out_report_bytes[44] = self.player_leds_enable

        out_report_bytes[45] = self.lightbar_red
        out_report_bytes[46] = self.lightbar_green
        out_report_bytes[47] = self.lightbar_blue

        return out_report_bytes
