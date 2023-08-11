from tests.mock.InRep import InRep


class InRepBt01(InRep):

    def __init__(self):
        super().__init__(raw_bytes=bytearray(
            b'\x01\x80\x80\x82\x83\x00\x00\x9c\x08\x00'
        ))

    def set_axes_0(self, value: int):
        self._set_uint8(0, value)

    def set_axes_1(self, value: int):
        self._set_uint8(1, value)

    def set_axes_2(self, value: int):
        self._set_uint8(2, value)

    def set_axes_3(self, value: int):
        self._set_uint8(3, value)

    def set_buttons_0(self, value: int):
        self._set_uint8(4, value)

    def set_buttons_1(self, value: int):
        self._set_uint8(5, value)

    def set_buttons_2(self, value: int):
        self._set_uint8(6, value)

    def set_axes_4(self, value: int):
        self._set_uint8(7, value)

    def set_axes_5(self, value: int):
        self._set_uint8(8, value)

    def set_timestamp_3(self, value: int) -> None:
        raise NotImplementedError

    def set_timestamp_2(self, value: int) -> None:
        raise NotImplementedError

    def set_timestamp_1(self, value: int) -> None:
        raise NotImplementedError

    def set_buttons_3(self, value: int) -> None:
        raise NotImplementedError

    def set_timestamp_0(self, value: int) -> None:
        raise NotImplementedError

    def set_battery_1(self, value: int) -> None:
        raise NotImplementedError

    def set_accel_x_1(self, value: int) -> None:
        raise NotImplementedError

    def set_accel_y_0(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_1_2(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_1(self, value: int) -> None:
        raise NotImplementedError

    def set_accel_y_1(self, value: int) -> None:
        raise NotImplementedError

    def set_accel_z_0(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_1_3(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_2(self, value: int) -> None:
        raise NotImplementedError

    def set_accel_z_1(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_3(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_1_0(self, value: int) -> None:
        raise NotImplementedError

    def set_accel_x_0(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_1_1(self, value: int) -> None:
        raise NotImplementedError

    def set_touch_2_0(self, value: int) -> None:
        raise NotImplementedError

    def set_gyro_x_1(self, value: int) -> None:
        raise NotImplementedError

    def set_gyro_y_0(self, value: int) -> None:
        raise NotImplementedError

    def set_gyro_x_0(self, value: int) -> None:
        raise NotImplementedError

    def set_gyro_z_1(self, value: int) -> None:
        raise NotImplementedError

    def set_gyro_y_1(self, value: int) -> None:
        raise NotImplementedError

    def set_gyro_z_0(self, value: int) -> None:
        raise NotImplementedError

    def set_seq_num(self, value: int) -> None:
        raise NotImplementedError

    def set_l2_feedback(self, value: int) -> None:
        raise NotImplementedError

    def set_battery_0(self, value: int) -> None:
        raise NotImplementedError

    def set_r2_feedback(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_0(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_1(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_2(self, value: int) -> None:
        raise NotImplementedError

    def set_sensor_timestamp_3(self, value: int) -> None:
        raise NotImplementedError
