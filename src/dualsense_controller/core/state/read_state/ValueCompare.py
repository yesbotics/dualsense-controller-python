from typing import Final

from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Feedback, Gyroscope, JoyStick, \
    Orientation, TouchFinger
from dualsense_controller.core.state.typedef import CompareResult, Number

_HALF_255: Final[Number] = 127.5


class ValueCompare:

    @staticmethod
    def compare_joystick(
            before: JoyStick | None,
            after: JoyStick,
            deadzone_raw: Number = 0,
    ) -> CompareResult:
        if before is None:
            return True, after
        if deadzone_raw > 0 and (((after.x - _HALF_255) ** 2) + ((after.y - _HALF_255) ** 2)) <= (deadzone_raw ** 2):
            after = JoyStick(_HALF_255, _HALF_255)

        changed: bool = after.x != before.x or after.y != before.y
        return changed, after

    @staticmethod
    def compare_trigger(
            before: int | None,
            after: int,
            deadzone_raw: Number = 0,
    ) -> CompareResult:
        if before is None:
            return True, after
        if deadzone_raw > 0 and after <= deadzone_raw:
            after = 0
        changed: bool = after != before
        return changed, after

    @staticmethod
    # TODO: refact that compare fcts
    def compare_gyroscope(
            before: Gyroscope,
            after: Gyroscope,
            threshold_raw: Number = 0
    ) -> CompareResult:
        if before is None:
            return True, after
        if threshold_raw > 0:
            if abs(after.x - before.x) < threshold_raw \
                    and abs(after.y - before.y) < threshold_raw \
                    and abs(after.z - before.z) < threshold_raw:
                after = Gyroscope(before.x, before.y, before.z)
        changed: bool = after.x != before.x or after.y != before.y or after.z != before.z
        return changed, after

    @staticmethod
    def compare_accelerometer(
            before: Accelerometer,
            after: Accelerometer,
            threshold_raw: Number = 0
    ) -> CompareResult:
        if before is None:
            return True, after
        if threshold_raw > 0:
            if abs(after.x - before.x) < threshold_raw \
                    and abs(after.y - before.y) < threshold_raw \
                    and abs(after.z - before.z) < threshold_raw:
                after = Gyroscope(before.x, before.y, before.z)
        changed: bool = after.x != before.x or after.y != before.y or after.z != before.z
        return changed, after

    @staticmethod
    def compare_touch_finger(
            before: TouchFinger,
            after: TouchFinger
    ) -> CompareResult:
        if before is None:
            return True, after
        changed: bool = after.active != before.active or after.x != before.x or after.y != before.y or after.id != before.id
        return changed, after

    @staticmethod
    def compare_battery(
            before: Battery,
            after: Battery
    ) -> CompareResult:
        if before is None:
            return True, after
        changed: bool = (
                after.level_percentage != before.level_percentage
                or after.full != before.full
                or after.charging != before.charging
        )
        return changed, after

    @staticmethod
    def compare_feedback(
            before: Feedback,
            after: Feedback
    ) -> CompareResult:
        if before is None:
            return True, after
        changed: bool = after.active != before.active or after.value != before.value
        return changed, after

    @staticmethod
    def compare_orientation(
            before: Orientation,
            after: Orientation,
            threshold_raw: Number = 0
    ) -> CompareResult:
        if before is None:
            return True, after
        if threshold_raw > 0:
            if abs(after.yaw - before.yaw) < threshold_raw \
                    and abs(after.pitch - before.pitch) < threshold_raw \
                    and abs(after.roll - before.roll) < threshold_raw:
                after = Orientation(before.yaw, before.pitch, before.roll)
        changed: bool = after.yaw != before.yaw or after.pitch != before.pitch or after.roll != before.roll
        return changed, after
