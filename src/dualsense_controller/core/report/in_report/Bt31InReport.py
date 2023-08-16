from dualsense_controller.core.report.in_report.InReport import InReport


# ??? byte 0
# ??? byte 7?
# ??? byte 11
# ??? bytes 28-32
# ??? byte 41
# ??? bytes 44-52
# ??? bytes 55-76
class Bt31InReport(InReport):

    def __init__(self, raw_bytes: bytearray = None):
        super().__init__({
            "axes_0": 1, "axes_1": 2, "axes_2": 3, "axes_3": 4, "axes_4": 5, "axes_5": 6,
            "buttons_0": 8, "buttons_1": 9, "buttons_2": 10,
            "timestamp_0": 12, "timestamp_1": 13, "timestamp_2": 14, "timestamp_3": 15,
            "gyro_x_0": 16, "gyro_x_1": 17, "gyro_y_0": 18, "gyro_y_1": 19, "gyro_z_0": 20, "gyro_z_1": 21,
            "accel_x_0": 22, "accel_x_1": 23, "accel_y_0": 24, "accel_y_1": 25, "accel_z_0": 26, "accel_z_1": 27,
            "touch_1_0": 33, "touch_1_1": 34, "touch_1_2": 35, "touch_1_3": 36,
            "touch_2_0": 37, "touch_2_1": 38, "touch_2_2": 39, "touch_2_3": 40,
            "right_trigger_feedback": 42, "left_trigger_feedback": 43,
            "battery_0": 53, "battery_1": 54,
        }, raw_bytes=raw_bytes)
