from dualsense_controller.core.report.out_report.OutReport import OutReport
from dualsense_controller.core.report.out_report.enum import OutReportLength


class Bt01OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> BT31")

        out_report_bytes: bytes = bytearray(OutReportLength.BT_31)
        return out_report_bytes
