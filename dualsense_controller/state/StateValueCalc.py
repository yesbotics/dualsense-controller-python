import math
import time
from typing import Final

from dualsense_controller.state import Accelerometer, Gyroscope, Orientation


class StateValueCalc:

    @classmethod
    def sensor_axis(cls, v1: int, v0: int) -> int:
        res: int = ((v1 << 8) | v0)
        if res > 0x7FFF:
            res -= 0x10000
        return res

    @classmethod
    def touch_active(cls, t_0: int) -> bool:
        return not (t_0 & 0x80)

    @classmethod
    def touch_id(cls, t_0: int) -> int:
        return t_0 & 0x7F

    @classmethod
    def touch_x(cls, t_2: int, t_1: int) -> int:
        return ((t_2 & 0x0F) << 8) | t_1

    @classmethod
    def touch_y(cls, t_3: int, t_2: int) -> int:
        return (t_3 << 4) | ((t_2 & 0xF0) >> 4)

    @classmethod
    def batt_level_percentage(cls, b: int) -> float:
        batt_level_raw: int = b & 0x0f
        if batt_level_raw > 8:
            batt_level_raw = 8
        batt_level: float = batt_level_raw / 8
        return batt_level * 100

    @classmethod
    def orientation_simple(cls, accel: Accelerometer) -> Orientation:
        accel_z: float = accel.z
        return Orientation(
            pitch=(math.atan2(-accel.y, -accel_z) + math.pi),
            roll=(math.atan2(-accel.x, -accel_z) + math.pi)
        )

    _ALPHA: Final[float] = 0.98
    _DT: Final[float] = 0.01
    _LAST_TIME: float = 0

    @classmethod
    def orientation_complementary_filter(
            cls,
            gyro: Gyroscope,
            accel: Accelerometer,
            previous_orientation: Orientation
    ) -> Orientation:
        gyro_x: float = gyro.x
        gyro_y: float = gyro.y
        gyro_z: float = gyro.z
        accel_x: float = accel.x
        accel_y: float = accel.y
        accel_z: float = accel.z

        new_time: float = time.perf_counter()
        dt: float = new_time - cls._LAST_TIME
        cls._LAST_TIME = new_time

        # print('g', gyro_x, gyro_y, gyro_z)
        # print('a', accel_x, accel_y, accel_z)

        # Calculate accelerometer angles
        roll_accel: float = math.atan2(accel_y, accel_z)
        pitch_accel: float = math.atan2(-accel_x, math.sqrt(accel_y ** 2 + accel_z ** 2))

        # Calculate gyroscope angles (integration)
        roll_gyro: float = previous_orientation.roll + gyro_x * dt
        pitch_gyro: float = previous_orientation.pitch + gyro_y * dt

        # Calculate the yaw using a complementary filter with limited yaw rate
        # The yaw is limited to prevent it from becoming unstable (negative infinity)
        yaw_gyro: float = previous_orientation.yaw + gyro_z * dt
        yaw_gyro = math.atan2(math.sin(yaw_gyro), math.cos(yaw_gyro))

        # Complementary filter to combine accelerometer and gyroscope data
        return Orientation(
            roll=cls._ALPHA * roll_gyro + (1 - cls._ALPHA) * roll_accel,
            pitch=cls._ALPHA * pitch_gyro + (1 - cls._ALPHA) * pitch_accel,
            yaw=yaw_gyro,  # Yaw is typically not estimated using accelerometer data alone
        )
