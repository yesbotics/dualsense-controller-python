from dualsense_controller.core.report.in_report.InReport import InReport


class Bt01InReport(InReport):
    def _update(self) -> None:
        self._axes_0 = self._get_uint8(0)
        self._axes_1 = self._get_uint8(1)
        self._axes_2 = self._get_uint8(2)
        self._axes_3 = self._get_uint8(3)
        self._buttons_0 = self._get_uint8(4)
        self._buttons_1 = self._get_uint8(5)
        self._buttons_2 = self._get_uint8(6)
        self._axes_4 = self._get_uint8(7)
        self._axes_5 = self._get_uint8(8)
