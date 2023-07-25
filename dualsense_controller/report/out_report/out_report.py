from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .enum import (
    OutReportId,
    OutFlagsPhysics,
    OutFlagsLights,
    OutLedOptions,
    OutPulseOptions,
    OutBrightness,
    OutPlayerLed,
    OutLightbarMode
)
from dualsense_controller.report import InReportLength
from dualsense_controller.util import clamp_byte


class OutReportLength(int, Enum):
    USB_01 = 48
    BT_31 = InReportLength.BT_31
    BT_01 = InReportLength.BT_01
    # USB_01 = 47
    # BT_31 = 77
    # BT_01 = 77  # ??


@dataclass(slots=True)
class OutReport(ABC):

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    flags_physics: int = OutFlagsPhysics.ALL
    flags_lights: int = OutFlagsLights.ALL

    lightbar_red: int = 0xff
    lightbar_green: int = 0xff
    lightbar_blue: int = 0xff

    motor_left: int = 0x00
    motor_right: int = 0x00

    l2_effect_mode: int = 0x26
    l2_effect_param1: int = 0x90
    l2_effect_param2: int = 0xA0
    l2_effect_param3: int = 0xFF
    l2_effect_param4: int = 0x00
    l2_effect_param5: int = 0x00
    l2_effect_param6: int = 0x00
    l2_effect_param7: int = 0x00

    r2_effect_mode: int = 0x26
    r2_effect_param1: int = 0x90
    r2_effect_param2: int = 0xA0
    r2_effect_param3: int = 0xFF
    r2_effect_param4: int = 0x00
    r2_effect_param5: int = 0x00
    r2_effect_param6: int = 0x00
    r2_effect_param7: int = 0x00

    lightbar: bool = True

    microphone_led: bool = False
    microphone_mute: bool = True

    led_options: OutLedOptions = OutLedOptions.ALL
    pulse_options: OutPulseOptions = OutPulseOptions.OFF
    brightness: OutBrightness = OutBrightness.HIGH
    player_led: int = OutPlayerLed.OFF


class Usb01OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> usb")

        # reportId = 0x02

        out_report_bytes: bytearray = bytearray(OutReportLength.USB_01)

        out_report_bytes[0] = OutReportId.USB_01

        #
        # valid_flag0 - flags determing what changes this packet will perform
        # or: OperatingMode
        #
        # bit 0: COMPATIBLE_VIBRATION
        # bit 1: HAPTICS_SELECT
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
        out_report_bytes[2] = self.flags_lights

        # DualShock 4 compatibility mode.
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
        # Mode
        # 0x00: off
        # 0x01: mode1
        # 0x02: mode2
        # 0x05: mode1 + mode4
        # 0x06: mode2 + mode4
        # 0x21: mode1 + mode20
        # 0x25: mode1 + mode4 + mode20
        # 0x26: mode2 + mode4 + mode20
        # 0xFC: calibration
        out_report_bytes[11] = self.r2_effect_mode
        out_report_bytes[12] = self.r2_effect_param1
        out_report_bytes[13] = self.r2_effect_param2
        out_report_bytes[14] = self.r2_effect_param3
        out_report_bytes[15] = self.r2_effect_param4
        out_report_bytes[16] = self.r2_effect_param5
        out_report_bytes[17] = self.r2_effect_param6
        out_report_bytes[20] = self.r2_effect_param7

        out_report_bytes[22] = self.l2_effect_mode
        out_report_bytes[23] = self.l2_effect_param1
        out_report_bytes[24] = self.l2_effect_param2
        out_report_bytes[25] = self.l2_effect_param3
        out_report_bytes[26] = self.l2_effect_param4
        out_report_bytes[27] = self.l2_effect_param5
        out_report_bytes[28] = self.l2_effect_param6
        out_report_bytes[31] = self.l2_effect_param7

        out_report_bytes[39] = self.led_options

        # Lightbar on/off
        out_report_bytes[41] = OutLightbarMode.LIGHT_ON if self.lightbar else OutLightbarMode.LIGHT_OUT

        # Disable/Endable LEDs or Pulse/Fade-Options?
        out_report_bytes[42] = self.pulse_options
        out_report_bytes[43] = self.brightness
        out_report_bytes[44] = self.player_led

        out_report_bytes[45] = self.lightbar_red
        out_report_bytes[46] = self.lightbar_green
        out_report_bytes[47] = self.lightbar_blue

        return out_report_bytes


class Bt01OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> BT01")

        out_report_bytes: bytes = bytearray(OutReportLength.BT_01)
        return out_report_bytes


class Bt31OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> BT31")

        out_report_bytes: bytes = bytearray(OutReportLength.BT_31)
        return out_report_bytes
