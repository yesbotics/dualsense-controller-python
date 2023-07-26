from .OutReport import OutReport
from .enum import OutReportLength


class Bt01OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> BT01")

        out_report_bytes: bytes = bytearray(OutReportLength.BT_01)
        return out_report_bytes


class Bt31OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> BT31")

        out_report_bytes: bytes = bytearray(OutReportLength.BT_31)
        return out_report_bytes