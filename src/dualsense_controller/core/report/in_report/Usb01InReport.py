from dualsense_controller.core.report.in_report.InReport import InReport


# ??? byte 31
# ??? byte 40
# ??? bytes 43-51
class Usb01InReport(InReport):
    def __init__(self, raw_bytes: bytearray = None):
        super().__init__({
            "axes_0": 0, "axes_1": 1, "axes_2": 2, "axes_3": 3, "axes_4": 4, "axes_5": 5,
            "seq_num": 6,
            "buttons_0": 7, "buttons_1": 8, "buttons_2": 9, "buttons_3": 10,
            "timestamp_0": 11, "timestamp_1": 12, "timestamp_2": 13, "timestamp_3": 14,
            "gyro_x_0": 15, "gyro_x_1": 16, "gyro_y_0": 17, "gyro_y_1": 18, "gyro_z_0": 19, "gyro_z_1": 20,
            "accel_x_0": 21, "accel_x_1": 22, "accel_y_0": 23, "accel_y_1": 24, "accel_z_0": 25, "accel_z_1": 26,
            "sensor_timestamp_0": 27, "sensor_timestamp_1": 28, "sensor_timestamp_2": 29, "sensor_timestamp_3": 30,
            "touch_0_0": 32, "touch_0_1": 33, "touch_0_2": 34, "touch_0_3": 35,
            "touch_1_0": 36, "touch_1_1": 37, "touch_1_2": 38, "touch_1_3": 39,
            "r2_feedback": 41, "l2_feedback": 42,
            "battery_0": 52, "battery_1": 53
        }, raw_bytes=raw_bytes)
