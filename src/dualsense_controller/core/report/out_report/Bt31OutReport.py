from dualsense_controller.core.report.out_report.OutReport import OutReport
from dualsense_controller.core.report.out_report.crc32 import compute_crc32_checksum
from dualsense_controller.core.report.out_report.enum import OutReportLength
from dualsense_controller.core.report.out_report.util import clamp_byte
from dualsense_controller.core.state.write_state.enum import LightbarMode


class Bt31OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> BT31")

        out_report_bytes: bytearray = bytearray(OutReportLength.BT_31)

        # report type
        out_report_bytes[0] = 0x31
        out_report_bytes[1] = self.operating_mode

        # report data
        out_report_bytes[2] = self.flags_physics
        out_report_bytes[3] = self.flags_controls

        # DualShock 4 compatibility update_level.
        out_report_bytes[4] = clamp_byte(self.motor_right)
        out_report_bytes[5] = clamp_byte(self.motor_left)

        out_report_bytes[10] = self.microphone_led
        out_report_bytes[11] = 0x10 if self.microphone_mute else 0x00

        out_report_bytes[12] = self.right_trigger_effect_mode
        out_report_bytes[13] = self.right_trigger_effect_param1
        out_report_bytes[14] = self.right_trigger_effect_param2
        out_report_bytes[15] = self.right_trigger_effect_param3
        out_report_bytes[16] = self.right_trigger_effect_param4
        out_report_bytes[17] = self.right_trigger_effect_param5
        out_report_bytes[18] = self.right_trigger_effect_param6
        out_report_bytes[21] = self.right_trigger_effect_param7

        out_report_bytes[23] = self.left_trigger_effect_mode
        out_report_bytes[24] = self.left_trigger_effect_param1
        out_report_bytes[25] = self.left_trigger_effect_param2
        out_report_bytes[26] = self.left_trigger_effect_param3
        out_report_bytes[27] = self.left_trigger_effect_param4
        out_report_bytes[28] = self.left_trigger_effect_param5
        out_report_bytes[29] = self.left_trigger_effect_param6
        out_report_bytes[32] = self.left_trigger_effect_param7

        out_report_bytes[40] = self.led_options
        out_report_bytes[41] = LightbarMode.LIGHT_ON if self.lightbar_on_off else LightbarMode.LIGHT_OFF

        out_report_bytes[43] = self.lightbar_pulse_options
        out_report_bytes[44] = self.player_leds_brightness
        out_report_bytes[45] = self.player_leds_enable

        out_report_bytes[46] = self.lightbar_red
        out_report_bytes[47] = self.lightbar_green
        out_report_bytes[48] = self.lightbar_blue

        crc32_checksum_result: int = compute_crc32_checksum(out_report_bytes)

        out_report_bytes[74] = (crc32_checksum_result & 0x000000FF)
        out_report_bytes[75] = (crc32_checksum_result & 0x0000FF00) >> 8
        out_report_bytes[76] = (crc32_checksum_result & 0x00FF0000) >> 16
        out_report_bytes[77] = (crc32_checksum_result & 0xFF000000) >> 24

        return out_report_bytes
