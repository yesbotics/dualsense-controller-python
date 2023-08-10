from tests.mock.in_rep.InRep import InRep


class InRepBt31(InRep):

    def __init__(self):
        super().__init__(raw_bytes=bytearray(
            b'1\x01\x80\x81\x82\x83\x00\x00\x01\x08\x00\x00\x00\xae\xab\x8b\xf2'
            b'\x02\x00\xfc\xff\x02\x00\xdc\xff\xda\x1e\x9e\x06\xc7\xb5\xe4\x00\x08'
            b'\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\t\x00\x00\x00\x00\x00\xc3\xc9\xe4'
            b'\x00\t\x00\x00\xaf\xc5\x1af\xc2\xf3\x16\xbd\x00\x00\x00\x00\x00\x00\x00\x00\x00B\xd7\xd8\r'
        ))

    def set_axes_0(self, value: int) -> None:
        self._set_uint8(1, value)

    def set_axes_1(self, value: int) -> None:
        self._set_uint8(2, value)

    def set_axes_2(self, value: int) -> None:
        self._set_uint8(3, value)

    def set_axes_3(self, value: int) -> None:
        self._set_uint8(4, value)

    def set_axes_4(self, value: int) -> None:
        self._set_uint8(5, value)

    def set_axes_5(self, value: int) -> None:
        self._set_uint8(6, value)

    def set_buttons_0(self, value: int) -> None:
        self._set_uint8(8, value)

    def set_buttons_1(self, value: int) -> None:
        self._set_uint8(9, value)

    def set_buttons_2(self, value: int) -> None:
        self._set_uint8(10, value)

    def set_timestamp_0(self, value: int) -> None:
        self._set_uint8(12, value)

    def set_timestamp_1(self, value: int) -> None:
        self._set_uint8(13, value)

    def set_timestamp_2(self, value: int) -> None:
        self._set_uint8(14, value)

    def set_timestamp_3(self, value: int) -> None:
        self._set_uint8(15, value)

    def set_gyro_x_0(self, value: int) -> None:
        self._set_uint8(16, value)

    def set_gyro_x_1(self, value: int) -> None:
        self._set_uint8(17, value)

    def set_gyro_y_0(self, value: int) -> None:
        self._set_uint8(18, value)

    def set_gyro_y_1(self, value: int) -> None:
        self._set_uint8(19, value)

    def set_gyro_z_0(self, value: int) -> None:
        self._set_uint8(20, value)

    def set_gyro_z_1(self, value: int) -> None:
        self._set_uint8(21, value)

    def set_accel_x_0(self, value: int) -> None:
        self._set_uint8(22, value)

    def set_accel_x_1(self, value: int) -> None:
        self._set_uint8(23, value)

    def set_accel_y_0(self, value: int) -> None:
        self._set_uint8(24, value)

    def set_accel_y_1(self, value: int) -> None:
        self._set_uint8(25, value)

    def set_accel_z_0(self, value: int) -> None:
        self._set_uint8(26, value)

    def set_accel_z_1(self, value: int) -> None:
        self._set_uint8(27, value)

    def set_touch_0_0(self, value: int) -> None:
        self._set_uint8(33, value)

    def set_touch_0_1(self, value: int) -> None:
        self._set_uint8(34, value)

    def set_touch_0_2(self, value: int) -> None:
        self._set_uint8(35, value)

    def set_touch_0_3(self, value: int) -> None:
        self._set_uint8(36, value)

    def set_touch_1_0(self, value: int) -> None:
        self._set_uint8(37, value)

    def set_touch_1_1(self, value: int) -> None:
        self._set_uint8(38, value)

    def set_touch_1_2(self, value: int) -> None:
        self._set_uint8(39, value)

    def set_touch_1_3(self, value: int) -> None:
        self._set_uint8(40, value)

    def set_r2_feedback(self, value: int) -> None:
        self._set_uint8(42, value)

    def set_l2_feedback(self, value: int) -> None:
        self._set_uint8(43, value)

    def set_battery_0(self, value: int) -> None:
        self._set_uint8(53, value)

    def set_battery_1(self, value: int) -> None:
        self._set_uint8(54, value)

    def set_buttons_3(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_1(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_2(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_3(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_0(self, value: int) -> None:
        raise NotImplementedError

    def set_seq_num(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_0(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_1(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_2(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_3(self, value: int) -> None:
        raise NotImplementedError
