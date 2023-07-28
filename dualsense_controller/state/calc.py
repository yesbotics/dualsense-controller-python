import numpy as np
from pyquaternion import Quaternion

from dualsense_controller.state import Accelerometer, Gyroscope, Orientation


def _calc_sensor_axis(v1: int, v0: int) -> int:
    sub: int = ((v1 << 8) | v0)
    return sub if sub > 0x7FFF else sub - 0x10000


def calc_gyroscope(x1: int, x0: int, y1: int, y0: int, z1: int, z0: int) -> Gyroscope:
    return Gyroscope(
        x=_calc_sensor_axis(x1, x0),
        y=_calc_sensor_axis(y1, y0),
        z=_calc_sensor_axis(z1, z0),
    )


def calc_accelerometer(x1: int, x0: int, y1: int, y0: int, z1: int, z0: int) -> Accelerometer:
    return Accelerometer(
        x=_calc_sensor_axis(x1, x0),
        y=_calc_sensor_axis(y1, y0),
        z=_calc_sensor_axis(z1, z0),
    )


def calc_touch_id(t_0: int) -> int:
    return t_0 & 0x7F


def calc_touch_x(t_2: int, t_1: int) -> int:
    return ((t_2 & 0x0F) << 8) | t_1


def calc_touch_y(t_3: int, t_2: int) -> int:
    return (t_3 << 4) | ((t_2 & 0xF0) >> 4)


def calc_batt_level_percentage(b: int) -> float:
    batt_level_raw: int = b & 0x0f
    if batt_level_raw > 8:
        batt_level_raw = 8
    batt_level: float = batt_level_raw / 8
    return batt_level * 100


def calc_orientation(gyro: Gyroscope, accel: Accelerometer) -> Orientation:
    # o = _calculate_orientation(
    #     [self._gyroscope_x.value],
    #     [self._gyroscope_y.value],
    #     [self._gyroscope_z.value],
    #     self._accelerometer_x.value,
    #     self._accelerometer_y.value,
    #     self._accelerometer_z.value,
    # )
    # orientation: Orientation = Orientation(
    #     yaw=0,
    #     pitch=0,
    #     roll=0,
    # )
    # self._orientation.value = orientation
    return Orientation(
        yaw=0,
        pitch=0,
        roll=0,
    )


def _calculate_orientation(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sample_period=0.01, alpha=0.98):
    # Normalize the accelerometer data
    norm_accel = np.sqrt(accel_x ** 2 + accel_y ** 2 + accel_z ** 2)
    accel_x /= norm_accel
    accel_y /= norm_accel
    accel_z /= norm_accel

    # Calculate the accelerometer pitch and roll angles
    pitch = np.arcsin(accel_x)
    roll = np.arctan2(-accel_y, accel_z)

    # Initialize the orientation quaternion representing the current orientation
    orientation = Quaternion(axis=[1, 0, 0], angle=pitch) * Quaternion(axis=[0, 1, 0], angle=roll)

    # Apply the complementary filter
    for gyro_x_val, gyro_y_val, gyro_z_val in zip(gyro_x, gyro_y, gyro_z):
        gyro_data_rad_per_sec = np.radians([gyro_x_val, gyro_y_val, gyro_z_val])

        # Integrate the gyroscope data to update orientation quaternion
        orientation = orientation * Quaternion(axis=gyro_data_rad_per_sec, angle=sample_period)
        orientation = orientation.normalised

        # Correct the orientation with the accelerometer measurements
        orientation_acc = Quaternion(axis=[1, 0, 0], angle=pitch) * Quaternion(axis=[0, 1, 0], angle=roll)
        orientation = Quaternion.slerp(orientation_acc, orientation, alpha)

    return orientation

# # Example usage
# gyro_x_value = 0.1  # Replace with your gyro_x data (single value)
# gyro_y_value = -0.2  # Replace with your gyro_y data (single value)
# gyro_z_value = 0.3  # Replace with your gyro_z data (single value)
# accel_x_value = 0.5  # Replace with your accel_x data (single value)
# accel_y_value = 0.1  # Replace with your accel_y data (single value)
# accel_z_value = -0.1  # Replace with your accel_z data (single value)
# sample_period_seconds = 0.01  # Replace with your sample period in seconds
#
# orientation = calculate_orientation([gyro_x_value], [gyro_y_value], [gyro_z_value], accel_x_value, accel_y_value, accel_z_value, sample_period_seconds)
# print("Estimated orientation quaternion:", orientation)
