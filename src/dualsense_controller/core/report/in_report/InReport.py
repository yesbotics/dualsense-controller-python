from abc import ABC, abstractmethod
from typing import Final

_IndexDict = dict[str, int]


class InReport(ABC):
    _OFFSET: Final[int] = 1

    @property
    def raw_bytes(self) -> bytes:
        return self._raw_bytes

    def __init__(self, index_dict: _IndexDict, raw_bytes: bytearray = None):
        self._index_dict: Final[_IndexDict] = index_dict
        self._raw_bytes: bytes | bytearray | None = raw_bytes

    def update(self, raw_bytes: bytes) -> None:
        self._raw_bytes = raw_bytes

    def _get_uint8(self, key: str) -> int:
        return self._raw_bytes[InReport._OFFSET + self._index_dict.get(key)]

    def _set_uint8(self, key: str, value: int) -> None:
        self._raw_bytes[InReport._OFFSET + self._index_dict.get(key)] = value

    # ########################################## GET ##########################################

    @property
    def axes_0(self) -> int:
        return self._get_uint8('axes_0')

    @property
    def axes_1(self) -> int:
        return self._get_uint8('axes_1')

    @property
    def axes_2(self) -> int:
        return self._get_uint8('axes_2')

    @property
    def axes_3(self) -> int:
        return self._get_uint8('axes_3')

    @property
    def axes_4(self) -> int:
        return self._get_uint8('axes_4')

    @property
    def axes_5(self) -> int:
        return self._get_uint8('axes_5')

    @property
    def seq_num(self) -> int:
        return self._get_uint8('seq_num')

    @property
    def buttons_0(self) -> int:
        return self._get_uint8('buttons_0')

    @property
    def buttons_1(self) -> int:
        return self._get_uint8('buttons_1')

    @property
    def buttons_2(self) -> int:
        return self._get_uint8('buttons_2')

    @property
    def buttons_3(self) -> int:
        return self._get_uint8('buttons_3')

    @property
    def timestamp_0(self) -> int:
        return self._get_uint8('timestamp_0')

    @property
    def timestamp_1(self) -> int:
        return self._get_uint8('timestamp_1')

    @property
    def timestamp_2(self) -> int:
        return self._get_uint8('timestamp_2')

    @property
    def timestamp_3(self) -> int:
        return self._get_uint8('timestamp_3')

    @property
    def gyro_x_0(self) -> int:
        return self._get_uint8('gyro_x_0')

    @property
    def gyro_x_1(self) -> int:
        return self._get_uint8('gyro_x_1')

    @property
    def gyro_y_0(self) -> int:
        return self._get_uint8('gyro_y_0')

    @property
    def gyro_y_1(self) -> int:
        return self._get_uint8('gyro_y_1')

    @property
    def gyro_z_0(self) -> int:
        return self._get_uint8('gyro_z_0')

    @property
    def gyro_z_1(self) -> int:
        return self._get_uint8('gyro_z_1')

    @property
    def accel_x_0(self) -> int:
        return self._get_uint8('accel_x_0')

    @property
    def accel_x_1(self) -> int:
        return self._get_uint8('accel_x_1')

    @property
    def accel_y_0(self) -> int:
        return self._get_uint8('accel_y_0')

    @property
    def accel_y_1(self) -> int:
        return self._get_uint8('accel_y_1')

    @property
    def accel_z_0(self) -> int:
        return self._get_uint8('accel_z_0')

    @property
    def accel_z_1(self) -> int:
        return self._get_uint8('accel_z_1')

    @property
    def sensor_timestamp_0(self) -> int:
        return self._get_uint8('sensor_timestamp_0')

    @property
    def sensor_timestamp_1(self) -> int:
        return self._get_uint8('sensor_timestamp_1')

    @property
    def sensor_timestamp_2(self) -> int:
        return self._get_uint8('sensor_timestamp_2')

    @property
    def sensor_timestamp_3(self) -> int:
        return self._get_uint8('sensor_timestamp_3')

    @property
    def touch_1_0(self) -> int:
        return self._get_uint8('touch_1_0')

    @property
    def touch_1_1(self) -> int:
        return self._get_uint8('touch_1_1')

    @property
    def touch_1_2(self) -> int:
        return self._get_uint8('touch_1_2')

    @property
    def touch_1_3(self) -> int:
        return self._get_uint8('touch_1_3')

    @property
    def touch_2_0(self) -> int:
        return self._get_uint8('touch_2_0')

    @property
    def touch_2_1(self) -> int:
        return self._get_uint8('touch_2_1')

    @property
    def touch_2_2(self) -> int:
        return self._get_uint8('touch_2_2')

    @property
    def touch_2_3(self) -> int:
        return self._get_uint8('touch_2_3')

    @property
    def right_trigger_feedback(self) -> int:
        return self._get_uint8('right_trigger_feedback')

    @property
    def left_trigger_feedback(self) -> int:
        return self._get_uint8('left_trigger_feedback')

    @property
    def battery_0(self) -> int:
        return self._get_uint8('battery_0')

    @property
    def battery_1(self) -> int:
        return self._get_uint8('battery_1')

    # ########################################## SET ONLY NEEDED FOR TESTING ########################################

    @axes_0.setter
    def axes_0(self, axes_0: int) -> None:
        self._set_uint8('axes_0', axes_0)

    @axes_1.setter
    def axes_1(self, axes_1: int) -> None:
        self._set_uint8('axes_1', axes_1)

    @axes_2.setter
    def axes_2(self, axes_2: int) -> None:
        self._set_uint8('axes_2', axes_2)

    @axes_3.setter
    def axes_3(self, axes_3: int) -> None:
        self._set_uint8('axes_3', axes_3)

    @axes_4.setter
    def axes_4(self, axes_4: int) -> None:
        self._set_uint8('axes_4', axes_4)

    @axes_5.setter
    def axes_5(self, axes_5: int) -> None:
        self._set_uint8('axes_5', axes_5)

    @seq_num.setter
    def seq_num(self, seq_num: int) -> None:
        self._set_uint8('seq_num', seq_num)

    @buttons_0.setter
    def buttons_0(self, buttons_0: int) -> None:
        self._set_uint8('buttons_0', buttons_0)

    @buttons_1.setter
    def buttons_1(self, buttons_1: int) -> None:
        self._set_uint8('buttons_1', buttons_1)

    @buttons_2.setter
    def buttons_2(self, buttons_2: int) -> None:
        self._set_uint8('buttons_2', buttons_2)

    @buttons_3.setter
    def buttons_3(self, buttons_3: int) -> None:
        self._set_uint8('buttons_3', buttons_3)

    @timestamp_0.setter
    def timestamp_0(self, timestamp_0: int) -> None:
        self._set_uint8('timestamp_0', timestamp_0)

    @timestamp_1.setter
    def timestamp_1(self, timestamp_1: int) -> None:
        self._set_uint8('timestamp_1', timestamp_1)

    @timestamp_2.setter
    def timestamp_2(self, timestamp_2: int) -> None:
        self._set_uint8('timestamp_2', timestamp_2)

    @timestamp_3.setter
    def timestamp_3(self, timestamp_3: int) -> None:
        self._set_uint8('timestamp_3', timestamp_3)

    @gyro_x_0.setter
    def gyro_x_0(self, gyro_x_0: int) -> None:
        self._set_uint8('gyro_x_0', gyro_x_0)

    @gyro_x_1.setter
    def gyro_x_1(self, gyro_x_1: int) -> None:
        self._set_uint8('gyro_x_1', gyro_x_1)

    @gyro_y_0.setter
    def gyro_y_0(self, gyro_y_0: int) -> None:
        self._set_uint8('gyro_y_0', gyro_y_0)

    @gyro_y_1.setter
    def gyro_y_1(self, gyro_y_1: int) -> None:
        self._set_uint8('gyro_y_1', gyro_y_1)

    @gyro_z_0.setter
    def gyro_z_0(self, gyro_z_0: int) -> None:
        self._set_uint8('gyro_z_0', gyro_z_0)

    @gyro_z_1.setter
    def gyro_z_1(self, gyro_z_1: int) -> None:
        self._set_uint8('gyro_z_1', gyro_z_1)

    @accel_x_0.setter
    def accel_x_0(self, accel_x_0: int) -> None:
        self._set_uint8('accel_x_0', accel_x_0)

    @accel_x_1.setter
    def accel_x_1(self, accel_x_1: int) -> None:
        self._set_uint8('accel_x_1', accel_x_1)

    @accel_y_0.setter
    def accel_y_0(self, accel_y_0: int) -> None:
        self._set_uint8('accel_y_0', accel_y_0)

    @accel_y_1.setter
    def accel_y_1(self, accel_y_1: int) -> None:
        self._set_uint8('accel_y_1', accel_y_1)

    @accel_z_0.setter
    def accel_z_0(self, accel_z_0: int) -> None:
        self._set_uint8('accel_z_0', accel_z_0)

    @accel_z_1.setter
    def accel_z_1(self, accel_z_1: int) -> None:
        self._set_uint8('accel_z_1', accel_z_1)

    @sensor_timestamp_0.setter
    def sensor_timestamp_0(self, sensor_timestamp_0: int) -> None:
        self._set_uint8('sensor_timestamp_0', sensor_timestamp_0)

    @sensor_timestamp_1.setter
    def sensor_timestamp_1(self, sensor_timestamp_1: int) -> None:
        self._set_uint8('sensor_timestamp_1', sensor_timestamp_1)

    @sensor_timestamp_2.setter
    def sensor_timestamp_2(self, sensor_timestamp_2: int) -> None:
        self._set_uint8('sensor_timestamp_2', sensor_timestamp_2)

    @sensor_timestamp_3.setter
    def sensor_timestamp_3(self, sensor_timestamp_3: int) -> None:
        self._set_uint8('sensor_timestamp_3', sensor_timestamp_3)

    @touch_1_0.setter
    def touch_1_0(self, touch_1_0: int) -> None:
        self._set_uint8('touch_1_0', touch_1_0)

    @touch_1_1.setter
    def touch_1_1(self, touch_1_1: int) -> None:
        self._set_uint8('touch_1_1', touch_1_1)

    @touch_1_2.setter
    def touch_1_2(self, touch_1_2: int) -> None:
        self._set_uint8('touch_1_2', touch_1_2)

    @touch_1_3.setter
    def touch_1_3(self, touch_1_3: int) -> None:
        self._set_uint8('touch_1_3', touch_1_3)

    @touch_2_0.setter
    def touch_2_0(self, touch_2_0: int) -> None:
        self._set_uint8('touch_2_0', touch_2_0)

    @touch_2_1.setter
    def touch_2_1(self, touch_2_1: int) -> None:
        self._set_uint8('touch_2_1', touch_2_1)

    @touch_2_2.setter
    def touch_2_2(self, touch_2_2: int) -> None:
        self._set_uint8('touch_2_2', touch_2_2)

    @touch_2_3.setter
    def touch_2_3(self, touch_2_3: int) -> None:
        self._set_uint8('touch_2_3', touch_2_3)

    @right_trigger_feedback.setter
    def right_trigger_feedback(self, right_trigger_feedback: int) -> None:
        self._set_uint8('right_trigger_feedback', right_trigger_feedback)

    @left_trigger_feedback.setter
    def left_trigger_feedback(self, left_trigger_feedback: int) -> None:
        self._set_uint8('left_trigger_feedback', left_trigger_feedback)

    @battery_0.setter
    def battery_0(self, battery_0: int) -> None:
        self._set_uint8('battery_0', battery_0)

    @battery_1.setter
    def battery_1(self, battery_1: int) -> None:
        self._set_uint8('battery_1', battery_1)
