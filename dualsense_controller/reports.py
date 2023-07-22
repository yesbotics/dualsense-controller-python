from abc import ABC, abstractmethod
from typing import Final


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

