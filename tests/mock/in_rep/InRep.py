from abc import abstractmethod, ABC
from typing import Final


class InRep(ABC):
    _OFFSET: int = 1

    @property
    def raw_bytes(self) -> bytearray:
        return self._raw_bytes

    def __init__(self, raw_bytes: bytearray):
        self._raw_bytes: Final[bytearray] = raw_bytes

    def _set_uint8(self, index, value: int) -> None:
        self._raw_bytes[InRep._OFFSET + index] = value

    @abstractmethod
    def set_buttons_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_buttons_2(self, value: int) -> None:
        pass

    @abstractmethod
    def set_timestamp_3(self, value: int) -> None:
        pass

    @abstractmethod
    def set_buttons_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_timestamp_2(self, value: int) -> None:
        pass

    @abstractmethod
    def set_timestamp_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_buttons_3(self, value: int) -> None:
        pass

    @abstractmethod
    def set_timestamp_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_battery_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_accel_x_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_accel_y_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_1_2(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_2_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_accel_y_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_accel_z_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_1_3(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_2_2(self, value: int) -> None:
        pass

    @abstractmethod
    def set_accel_z_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_2_3(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_1_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_accel_x_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_1_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_touch_2_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_gyro_x_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_gyro_y_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_gyro_x_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_gyro_z_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_gyro_y_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_gyro_z_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_seq_num(self, value: int) -> None:
        pass

    @abstractmethod
    def set_l2_feedback(self, value: int) -> None:
        pass

    @abstractmethod
    def set_battery_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_r2_feedback(self, value: int) -> None:
        pass

    @abstractmethod
    def set_axes_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_axes_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_axes_2(self, value: int) -> None:
        pass

    @abstractmethod
    def set_axes_3(self, value: int) -> None:
        pass

    @abstractmethod
    def set_axes_4(self, value: int) -> None:
        pass

    @abstractmethod
    def set_sensor_timestamp_0(self, value: int) -> None:
        pass

    @abstractmethod
    def set_axes_5(self, value: int) -> None:
        pass

    @abstractmethod
    def set_sensor_timestamp_1(self, value: int) -> None:
        pass

    @abstractmethod
    def set_sensor_timestamp_2(self, value: int) -> None:
        pass

    @abstractmethod
    def set_sensor_timestamp_3(self, value: int) -> None:
        pass
