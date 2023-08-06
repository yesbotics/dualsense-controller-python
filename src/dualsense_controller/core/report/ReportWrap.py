from threading import Lock
from typing import Final

from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.report.out_report.OutReport import OutReport

_Report = InReport | OutReport


class ReportWrap:

    def __init__(self):
        self._report: _Report | None = None
        self._lock: Final[Lock] = Lock()

    @property
    def report(self) -> _Report | None:
        with self._lock:
            return self._report

    @report.setter
    def report(self, report: _Report) -> None:
        with self._lock:
            self._report = report
