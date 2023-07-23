from abc import ABC, abstractmethod
from typing import Final

from dualsense_controller.common import OutReportLength, OutReportId, OutFlagsPhysics, OutFlagsLights, \
    OutLedOptions, \
    OutPulseOptions, OutBrightness, OutPlayerLed, OutLightbarMode


class OutReport(ABC):

    def __init__(self):
        self.flags_physics: int = OutFlagsPhysics.ALL
        self.flags_lights: int = OutFlagsLights.ALL

        self.lightbar_red: int = 0xff
        self.lightbar_green: int = 0xff
        self.lightbar_blue: int = 0xff

        self.motor_left: int = 0x00
        self.motor_right: int = 0x00

        self.l2_effect_mode: int = 0x26
        self.l2_effect_param1: int = 0x90
        self.l2_effect_param2: int = 0xA0
        self.l2_effect_param3: int = 0xFF
        self.l2_effect_param4: int = 0x00
        self.l2_effect_param5: int = 0x00
        self.l2_effect_param6: int = 0x00
        self.l2_effect_param7: int = 0x00

        self.r2_effect_mode: int = 0x26
        self.r2_effect_param1: int = 0x90
        self.r2_effect_param2: int = 0xA0
        self.r2_effect_param3: int = 0xFF
        self.r2_effect_param4: int = 0x00
        self.r2_effect_param5: int = 0x00
        self.r2_effect_param6: int = 0x00
        self.r2_effect_param7: int = 0x00

        self.lightbar: bool = True

        self.microphone_led: bool = False
        self.microphone_mute: bool = True

        self.led_options: OutLedOptions = OutLedOptions.ALL
        self.pulse_options: OutPulseOptions = OutPulseOptions.OFF
        self.brightness: OutBrightness = OutBrightness.HIGH
        self.player_led: int = OutPlayerLed.OFF

    @abstractmethod
    def to_bytes(self) -> bytearray:
        pass


class Usb01OutReport(OutReport):
    def to_bytes(self) -> bytearray:
        # print("-----------> usb")

        # reportId = 0x02

        out_report = bytearray(OutReportLength.USB_01)

        out_report[0] = OutReportId.USB_01

        #
        # valid_flag0 - flags determing what changes this packet will perform
        # or: OperatingMode
        #
        # bit 0: COMPATIBLE_VIBRATION
        # bit 1: HAPTICS_SELECT
        out_report[1] = self.flags_physics

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
        out_report[2] = self.flags_lights

        # DualShock 4 compatibility mode.
        out_report[3] = clamp_byte(self.motor_right)
        out_report[4] = clamp_byte(self.motor_left)

        # mute_button_led
        # 0: mute LED off
        # 1: mute LED on
        out_report[9] = self.microphone_led

        # power_save_control
        # bit 4: POWER_SAVE_CONTROL_MIC_MUTE
        out_report[10] = 0x10 if self.microphone_mute else 0x00

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
        out_report[11] = self.r2_effect_mode
        out_report[12] = self.r2_effect_param1
        out_report[13] = self.r2_effect_param2
        out_report[14] = self.r2_effect_param3
        out_report[15] = self.r2_effect_param4
        out_report[16] = self.r2_effect_param5
        out_report[17] = self.r2_effect_param6
        out_report[20] = self.r2_effect_param7

        out_report[22] = self.l2_effect_mode
        out_report[23] = self.l2_effect_param1
        out_report[24] = self.l2_effect_param2
        out_report[25] = self.l2_effect_param3
        out_report[26] = self.l2_effect_param4
        out_report[27] = self.l2_effect_param5
        out_report[28] = self.l2_effect_param6
        out_report[31] = self.l2_effect_param7

        out_report[39] = self.led_options

        # Lightbar on/off
        out_report[41] = OutLightbarMode.LIGHT_ON if self.lightbar else OutLightbarMode.LIGHT_OUT

        # Disable/Endable LEDs or Pulse/Fade-Options?
        out_report[42] = self.pulse_options
        out_report[43] = self.brightness
        out_report[44] = self.player_led

        out_report[45] = self.lightbar_red
        out_report[46] = self.lightbar_green
        out_report[47] = self.lightbar_blue

        return out_report


class Bt01OutReport(OutReport):
    def to_bytes(self) -> bytearray:
        # print("-----------> BT01")

        out_report = bytearray(OutReportLength.BT_01)
        return out_report


class Bt31OutReport(OutReport):
    def to_bytes(self) -> bytearray:
        # print("-----------> BT31")

        out_report = bytearray(OutReportLength.BT_31)
        return out_report


class InReport(ABC):

    def __init__(self, raw: bytes, offset: int):
        self.__raw: Final[bytes] = raw
        self.__offset: Final[int] = offset

        self._axes_0: int | None = None
        self._axes_1: int | None = None
        self._axes_2: int | None = None
        self._axes_3: int | None = None
        self._axes_4: int | None = None
        self._axes_5: int | None = None
        self._seq_num: int | None = None
        self._buttons_0: int | None = None
        self._buttons_1: int | None = None
        self._buttons_2: int | None = None
        self._buttons_3: int | None = None
        self._timestamp_0: int | None = None
        self._timestamp_1: int | None = None
        self._timestamp_2: int | None = None
        self._timestamp_3: int | None = None
        self._gyro_x_0: int | None = None
        self._gyro_x_1: int | None = None
        self._gyro_y_0: int | None = None
        self._gyro_y_1: int | None = None
        self._gyro_z_0: int | None = None
        self._gyro_z_1: int | None = None
        self._accel_x_0: int | None = None
        self._accel_x_1: int | None = None
        self._accel_y_0: int | None = None
        self._accel_y_1: int | None = None
        self._accel_z_0: int | None = None
        self._accel_z_1: int | None = None
        self._sensor_timestamp_0: int | None = None
        self._sensor_timestamp_1: int | None = None
        self._sensor_timestamp_2: int | None = None
        self._sensor_timestamp_3: int | None = None
        self._touch_0_0: int | None = None
        self._touch_0_1: int | None = None
        self._touch_0_2: int | None = None
        self._touch_0_3: int | None = None
        self._touch_1_0: int | None = None
        self._touch_1_1: int | None = None
        self._touch_1_2: int | None = None
        self._touch_1_3: int | None = None
        self._r2_feedback: int | None = None
        self._l2_feedback: int | None = None
        self._battery_0: int | None = None
        self._battery_1: int | None = None

        self._populate()

    @property
    def buttons_0(self) -> int:
        return self._buttons_0

    @property
    def buttons_2(self) -> int:
        return self._buttons_2

    @property
    def timestamp_3(self) -> int:
        return self._timestamp_3

    @property
    def buttons_1(self) -> int:
        return self._buttons_1

    @property
    def timestamp_2(self) -> int:
        return self._timestamp_2

    @property
    def timestamp_1(self) -> int:
        return self._timestamp_1

    @property
    def buttons_3(self) -> int:
        return self._buttons_3

    @property
    def timestamp_0(self) -> int:
        return self._timestamp_0

    @property
    def battery_1(self) -> int:
        return self._battery_1

    @property
    def accel_x_1(self) -> int:
        return self._accel_x_1

    @property
    def accel_y_0(self) -> int:
        return self._accel_y_0

    @property
    def touch_0_2(self) -> int:
        return self._touch_0_2

    @property
    def touch_1_1(self) -> int:
        return self._touch_1_1

    @property
    def accel_y_1(self) -> int:
        return self._accel_y_1

    @property
    def accel_z_0(self) -> int:
        return self._accel_z_0

    @property
    def touch_0_3(self) -> int:
        return self._touch_0_3

    @property
    def touch_1_2(self) -> int:
        return self._touch_1_2

    @property
    def accel_z_1(self) -> int:
        return self._accel_z_1

    @property
    def touch_1_3(self) -> int:
        return self._touch_1_3

    @property
    def touch_0_0(self) -> int:
        return self._touch_0_0

    @property
    def accel_x_0(self) -> int:
        return self._accel_x_0

    @property
    def touch_0_1(self) -> int:
        return self._touch_0_1

    @property
    def touch_1_0(self) -> int:
        return self._touch_1_0

    @property
    def gyro_x_1(self) -> int:
        return self._gyro_x_1

    @property
    def gyro_y_0(self) -> int:
        return self._gyro_y_0

    @property
    def gyro_x_0(self) -> int:
        return self._gyro_x_0

    @property
    def gyro_z_1(self) -> int:
        return self._gyro_z_1

    @property
    def gyro_y_1(self) -> int:
        return self._gyro_y_1

    @property
    def gyro_z_0(self) -> int:
        return self._gyro_z_0

    @property
    def seq_num(self) -> int:
        return self._seq_num

    @property
    def l2_feedback(self) -> int:
        return self._l2_feedback

    @property
    def battery_0(self) -> int:
        return self._battery_0

    @property
    def r2_feedback(self) -> int:
        return self._r2_feedback

    @property
    def axes_0(self) -> int:
        return self._axes_0

    @property
    def axes_1(self) -> int:
        return self._axes_1

    @property
    def axes_2(self) -> int:
        return self._axes_2

    @property
    def axes_3(self) -> int:
        return self._axes_3

    @property
    def axes_4(self) -> int:
        return self._axes_4

    @property
    def sensor_timestamp_0(self) -> int:
        return self._sensor_timestamp_0

    @property
    def axes_5(self) -> int:
        return self._axes_5

    @property
    def sensor_timestamp_1(self) -> int:
        return self._sensor_timestamp_1

    @property
    def sensor_timestamp_2(self) -> int:
        return self._sensor_timestamp_2

    @property
    def sensor_timestamp_3(self) -> int:
        return self._sensor_timestamp_3

    @property
    def raw(self) -> bytes:
        return self.__raw

    def _get(self, index: int) -> int:
        return self.__raw[self.__offset + index]

    @abstractmethod
    def _populate(self) -> None:
        pass


class Usb01InReport(InReport):
    def __init__(self, raw: bytes):
        super().__init__(raw, offset=1)

    def _populate(self) -> None:
        self._axes_0 = self._get(0)
        self._axes_1 = self._get(1)
        self._axes_2 = self._get(2)
        self._axes_3 = self._get(3)
        self._axes_4 = self._get(4)
        self._axes_5 = self._get(5)
        # self._seq_num = self.get(6)
        self._buttons_0 = self._get(7)
        self._buttons_1 = self._get(8)
        self._buttons_2 = self._get(9)
        # self._buttons_3 = self._get(10)
        # self._timestamp_0 = self.get(11)
        # self._timestamp_1 = self.get(12)
        # self._timestamp_2 = self.get(13)
        # self._timestamp_3 = self.get(14)
        self._gyro_x_0 = self._get(15)
        self._gyro_x_1 = self._get(16)
        self._gyro_y_0 = self._get(17)
        self._gyro_y_1 = self._get(18)
        self._gyro_z_0 = self._get(19)
        self._gyro_z_1 = self._get(20)
        self._accel_x_0 = self._get(21)
        self._accel_x_1 = self._get(22)
        self._accel_y_0 = self._get(23)
        self._accel_y_1 = self._get(24)
        self._accel_z_0 = self._get(25)
        self._accel_z_1 = self._get(26)
        # self._sensor_timestamp_0 = self.get(27)
        # self._sensor_timestamp_1 = self.get(28)
        # self._sensor_timestamp_2 = self.get(29)
        # self._sensor_timestamp_3 = self.get(30)
        # ??? byte 31
        self._touch_0_0 = self._get(32)
        self._touch_0_1 = self._get(33)
        self._touch_0_2 = self._get(34)
        self._touch_0_3 = self._get(35)
        self._touch_1_0 = self._get(36)
        self._touch_1_1 = self._get(37)
        self._touch_1_2 = self._get(38)
        self._touch_1_3 = self._get(39)
        # ??? byte 40
        self._r2_feedback = self._get(41)
        self._l2_feedback = self._get(42)
        # ??? bytes 43-51
        self._battery_0 = self._get(52)
        self._battery_1 = self._get(53)


class Bt31InReport(InReport):
    def __init__(self, raw: bytes):
        super().__init__(raw, offset=1)

    def _populate(self) -> None:
        # ??? byte 0
        self._axes_0 = self._get(1)
        self._axes_1 = self._get(2)
        self._axes_2 = self._get(3)
        self._axes_3 = self._get(4)
        self._axes_4 = self._get(5)
        self._axes_5 = self._get(6)
        # ??? byte 7?
        self._buttons_0 = self._get(8)
        self._buttons_1 = self._get(9)
        self._buttons_2 = self._get(10)
        # ??? byte 11
        # self._timestamp_0 = self._get(12)
        # self._timestamp_1 = self._get(13)
        # self._timestamp_2 = self._get(14)
        # self._timestamp_3 = self._get(15)
        self._gyro_x_0 = self._get(16)
        self._gyro_x_1 = self._get(17)
        self._gyro_y_0 = self._get(18)
        self._gyro_y_1 = self._get(19)
        self._gyro_z_0 = self._get(20)
        self._gyro_z_1 = self._get(21)
        self._accel_x_0 = self._get(22)
        self._accel_x_1 = self._get(23)
        self._accel_y_0 = self._get(24)
        self._accel_y_1 = self._get(25)
        self._accel_z_0 = self._get(26)
        self._accel_z_1 = self._get(27)
        # ??? bytes 28-32
        self._touch_0_0 = self._get(33)
        self._touch_0_1 = self._get(34)
        self._touch_0_2 = self._get(35)
        self._touch_0_3 = self._get(36)
        self._touch_1_0 = self._get(37)
        self._touch_1_1 = self._get(38)
        self._touch_1_2 = self._get(39)
        self._touch_1_3 = self._get(40)
        # ??? byte 41
        self._r2_feedback = self._get(42)
        self._l2_feedback = self._get(43)
        # ??? bytes 44-52
        self._battery_0 = self._get(53)
        self._battery_1 = self._get(54)
        # ??? bytes 55-76


class Bt01InReport(InReport):
    def __init__(self, raw: bytes):
        super().__init__(raw, offset=1)

    def _populate(self) -> None:
        self._axes_0 = self._get(0)
        self._axes_1 = self._get(1)
        self._axes_2 = self._get(2)
        self._axes_3 = self._get(3)
        self._buttons_0 = self._get(4)
        self._buttons_1 = self._get(5)
        self._buttons_2 = self._get(6)
        self._axes_4 = self._get(7)
        self._axes_5 = self._get(8)


def clamp(value: int, val_min: int, val_max: int) -> int:
    return min(val_max, max(val_min, value))


def clamp_byte(value: int) -> int:
    return min(255, max(0, value))
