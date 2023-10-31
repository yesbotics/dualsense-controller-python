from typing import Callable

from dualsense_controller.core.report.in_report.InReport import InReport

InReportCallback = Callable[[InReport], None]


