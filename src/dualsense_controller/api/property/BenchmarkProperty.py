from dualsense_controller.api.property.base import Property
from dualsense_controller.core.Benchmarker import Benchmark


class BenchmarkProperty(Property[Benchmark]):

    @property
    def value(self) -> Benchmark:
        return self._get_value()
