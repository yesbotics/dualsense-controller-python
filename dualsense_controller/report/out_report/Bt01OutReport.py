from .enum import OutReportLength
from .OutReport import OutReport


class Bt31OutReport(OutReport):
    def to_bytes(self) -> bytes:
        # print("-----------> BT31")

        out_report_bytes: bytes = bytearray(OutReportLength.BT_31)
        return out_report_bytes
