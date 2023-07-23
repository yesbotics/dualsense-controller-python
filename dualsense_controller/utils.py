import numpy as np
from pyquaternion import Quaternion

def calculate_orientation(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sample_period=0.01, alpha=0.98):
    # Normalize the accelerometer data
    norm_accel = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
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