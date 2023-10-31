from contextlib import contextmanager
from typing import Generator

from dualsense_controller.api.DualSenseController import DualSenseController, Mapping
from dualsense_controller.api.enum import UpdateLevel
from dualsense_controller.core.hidapi import DeviceInfo
from dualsense_controller.core.state.typedef import Number


@contextmanager
def active_dualsense_controller(
        # CORE
        device_index_or_device_info: int | DeviceInfo = 0,
        left_joystick_deadzone: Number = 0.05,
        right_joystick_deadzone: Number = 0.05,
        left_trigger_deadzone: Number = 0,
        right_trigger_deadzone: Number = 0,
        gyroscope_threshold: int = 0,
        accelerometer_threshold: int = 0,
        orientation_threshold: int = 0,
        mapping: Mapping = Mapping.NORMALIZED,
        update_level: UpdateLevel = UpdateLevel.DEFAULT,
        # OPTS
        microphone_initially_muted: bool = True,
        microphone_invert_led: bool = False,
) -> Generator[DualSenseController, None, None]:
    controller: DualSenseController = DualSenseController(
        device_index_or_device_info,
        left_joystick_deadzone=left_joystick_deadzone,
        right_joystick_deadzone=right_joystick_deadzone,
        left_trigger_deadzone=left_trigger_deadzone,
        right_trigger_deadzone=right_trigger_deadzone,
        gyroscope_threshold=gyroscope_threshold,
        accelerometer_threshold=accelerometer_threshold,
        orientation_threshold=orientation_threshold,
        mapping=mapping,
        update_level=update_level,
        microphone_initially_muted=microphone_initially_muted,
        microphone_invert_led=microphone_invert_led,
    )
    controller.activate()
    try:
        yield controller
    finally:
        controller.deactivate()
