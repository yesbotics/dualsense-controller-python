from collections import deque
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Final


@dataclass
class Benchmark:
    duration: float
    per_second: int


_ONE_SECOND_NS: Final[float] = 1e+9


class Benchmarker:
    def __init__(self, maxsize: int = 50):
        self._durations_queue: Final[deque] = deque(maxlen=maxsize)
        self._last_time: int | None = None

    def update(self) -> Benchmark | None:
        current: int = perf_counter_ns()
        if self._last_time is None:
            self._last_time = current
            return None
        duration: int = perf_counter_ns() - current
        self._last_time = current
        self._durations_queue.append(duration)

        sum_dur: int = 0
        for dur in self._durations_queue:
            sum_dur += dur

        duration_mean: float = sum_dur / len(self._durations_queue)
        return Benchmark(
            duration=duration_mean,
            per_second=int(_ONE_SECOND_NS / duration_mean)
        )
