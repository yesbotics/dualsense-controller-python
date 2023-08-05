from dualsense_controller.core.report.in_report.InReport import InReport


class InReportWrap:

    def __init__(self):
        self._in_report: InReport | None = None

    @property
    def in_report(self) -> InReport | None:
        return self._in_report

    def update(self, in_report: InReport) -> None:
        self._in_report = in_report
