from tests.mock.in_rep.InRep import InRep


class InRepUsb01(InRep):

    def __init__(self):
        super().__init__(raw_bytes=bytearray(
            b'\x01\x80\x80\x82\x83\x00\x00\x9c\x08\x00\x00\x00\x1c\x8f\xcc '
            b'\x03\x00\xfc\xff\x03\x00\xb0\xff\xeb\x1e\x82\x06\xbf@\xb1\t\x02'
            b'\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\t\x00\x00\x00\x00\x00\x03Z'
            b'\xb1\t)\x08\x00\xdd\xedU\xeb%{\x97\xc3'
        ))

    def set_axes_0(self, value: int) -> None:
        self._set_uint8(0, value)

    def set_axes_1(self, value: int) -> None:
        self._set_uint8(1, value)

    def set_axes_2(self, value: int) -> None:
        self._set_uint8(2, value)

    def set_axes_3(self, value: int) -> None:
        self._set_uint8(3, value)

    def set_axes_4(self, value: int) -> None:
        self._set_uint8(4, value)

    def set_axes_5(self, value: int) -> None:
        self._set_uint8(5, value)

    def set_seq_num(self, value: int) -> None:
        self._set_uint8(6, value)

    def set_buttons_0(self, value: int) -> None:
        self._set_uint8(7, value)

    def set_buttons_1(self, value: int) -> None:
        self._set_uint8(8, value)

    def set_buttons_2(self, value: int) -> None:
        self._set_uint8(9, value)

    def set_buttons_3(self, value: int) -> None:
        self._set_uint8(10, value)

    def set_timestamp_0(self, value: int) -> None:
        self._set_uint8(11, value)

    def set_timestamp_1(self, value: int) -> None:
        self._set_uint8(12, value)

    def set_timestamp_2(self, value: int) -> None:
        self._set_uint8(13, value)

    def set_timestamp_3(self, value: int) -> None:
        self._set_uint8(14, value)

    def set_gyro_x_0(self, value: int) -> None:
        self._set_uint8(15, value)

    def set_gyro_x_1(self, value: int) -> None:
        self._set_uint8(16, value)

    def set_gyro_y_0(self, value: int) -> None:
        self._set_uint8(17, value)

    def set_gyro_y_1(self, value: int) -> None:
        self._set_uint8(18, value)

    def set_gyro_z_0(self, value: int) -> None:
        self._set_uint8(19, value)

    def set_gyro_z_1(self, value: int) -> None:
        self._set_uint8(20, value)

    def set_accel_x_0(self, value: int) -> None:
        self._set_uint8(21, value)

    def set_accel_x_1(self, value: int) -> None:
        self._set_uint8(22, value)

    def set_accel_y_0(self, value: int) -> None:
        self._set_uint8(23, value)

    def set_accel_y_1(self, value: int) -> None:
        self._set_uint8(24, value)

    def set_accel_z_0(self, value: int) -> None:
        self._set_uint8(25, value)

    def set_accel_z_1(self, value: int) -> None:
        self._set_uint8(26, value)

    def set_sensor_timestamp_0(self, value: int) -> None:
        self._set_uint8(27, value)

    def set_sensor_timestamp_1(self, value: int) -> None:
        self._set_uint8(28, value)

    def set_sensor_timestamp_2(self, value: int) -> None:
        self._set_uint8(29, value)

    def set_sensor_timestamp_3(self, value: int) -> None:
        self._set_uint8(30, value)

    def set_touch_0_0(self, value: int) -> None:
        self._set_uint8(32, value)

    def set_touch_0_1(self, value: int) -> None:
        self._set_uint8(33, value)

    def set_touch_0_2(self, value: int) -> None:
        self._set_uint8(34, value)

    def set_touch_0_3(self, value: int) -> None:
        self._set_uint8(35, value)

    def set_touch_1_0(self, value: int) -> None:
        self._set_uint8(36, value)

    def set_touch_1_1(self, value: int) -> None:
        self._set_uint8(37, value)

    def set_touch_1_2(self, value: int) -> None:
        self._set_uint8(38, value)

    def set_touch_1_3(self, value: int) -> None:
        self._set_uint8(39, value)

    def set_r2_feedback(self, value: int) -> None:
        self._set_uint8(41, value)

    def set_l2_feedback(self, value: int) -> None:
        self._set_uint8(42, value)

    def set_battery_0(self, value: int) -> None:
        self._set_uint8(52, value)

    def set_battery_1(self, value: int) -> None:
        self._set_uint8(53, value)

    def set_touch_2_1(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_2(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_3(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_0(self, value: int) -> None:
        raise NotImplementedError
