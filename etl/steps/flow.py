from typing import Any

from etl.common import StepController


class Flow(StepController):
    def is_equal(self, value1: Any, value2: Any) -> bool:
        return value1 == value2

    def is_higher(self, value: Any, than: Any) -> bool:
        return value > than

    def is_equal_or_higher(self, value: Any, than: Any) -> bool:
        return value >= than
