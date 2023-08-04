from dualsense_controller.report.in_report.InReport import InReport


class Bt31InReport(InReport):

    def _update(self) -> None:
        # ??? byte 0
        self._axes_0 = self._get_uint8(1)
        self._axes_1 = self._get_uint8(2)
        self._axes_2 = self._get_uint8(3)
        self._axes_3 = self._get_uint8(4)
        self._axes_4 = self._get_uint8(5)
        self._axes_5 = self._get_uint8(6)
        # ??? byte 7?
        self._buttons_0 = self._get_uint8(8)
        self._buttons_1 = self._get_uint8(9)
        self._buttons_2 = self._get_uint8(10)
        # ??? byte 11
        # self._timestamp_0 = self._get(12)
        # self._timestamp_1 = self._get(13)
        # self._timestamp_2 = self._get(14)
        # self._timestamp_3 = self._get(15)
        self._gyro_x_0 = self._get_uint8(16)
        self._gyro_x_1 = self._get_uint8(17)
        self._gyro_y_0 = self._get_uint8(18)
        self._gyro_y_1 = self._get_uint8(19)
        self._gyro_z_0 = self._get_uint8(20)
        self._gyro_z_1 = self._get_uint8(21)
        self._accel_x_0 = self._get_uint8(22)
        self._accel_x_1 = self._get_uint8(23)
        self._accel_y_0 = self._get_uint8(24)
        self._accel_y_1 = self._get_uint8(25)
        self._accel_z_0 = self._get_uint8(26)
        self._accel_z_1 = self._get_uint8(27)
        # ??? bytes 28-32
        self._touch_0_0 = self._get_uint8(33)
        self._touch_0_1 = self._get_uint8(34)
        self._touch_0_2 = self._get_uint8(35)
        self._touch_0_3 = self._get_uint8(36)
        self._touch_1_0 = self._get_uint8(37)
        self._touch_1_1 = self._get_uint8(38)
        self._touch_1_2 = self._get_uint8(39)
        self._touch_1_3 = self._get_uint8(40)
        # ??? byte 41
        self._r2_feedback = self._get_uint8(42)
        self._l2_feedback = self._get_uint8(43)
        # ??? bytes 44-52
        self._battery_0 = self._get_uint8(53)
        self._battery_1 = self._get_uint8(54)
        # ??? bytes 55-76
