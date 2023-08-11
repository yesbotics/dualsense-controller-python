from dualsense_controller.core.report.in_report.InReport import InReport


class Bt01InReport(InReport):
    def __init__(self, raw_bytes: bytearray = None):
        super().__init__({
            "axes_0": 0, "axes_1": 1, "axes_2": 2, "axes_3": 3,
            "buttons_0": 4, "buttons_1": 5, "buttons_2": 6,
            "axes_4": 7, "axes_5": 8
        }, raw_bytes=raw_bytes)
