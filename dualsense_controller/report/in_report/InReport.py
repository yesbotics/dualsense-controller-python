from abc import ABC, abstractmethod
from typing import Final


class InReport(ABC):
    _OFFSET: Final[int] = 1

    @abstractmethod
    def _update(self) -> None:
        pass

    def __init__(self):
        self._raw_bytes: bytes | None = None

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
    def raw_bytes(self) -> bytes:
        return self._raw_bytes

    def update(self, raw_bytes: bytes) -> None:
        self._raw_bytes = raw_bytes
        self._update()

    def _get_uint8(self, index: int) -> int:
        return self._raw_bytes[InReport._OFFSET + index]
