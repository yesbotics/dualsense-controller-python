from dataclasses import dataclass

from dualsense_controller import DualSenseController, Mapping, Number, UpdateLevel
from tests.mock.MockedHidapiMockedHidapiDevice import MockedHidapiMockedHidapiDevice


@dataclass
class ControllerInstanceParams:
    mapping: Mapping = Mapping.DEFAULT
    update_level: UpdateLevel = UpdateLevel.DEFAULT
    left_joystick_deadzone: Number = 0
    right_joystick_deadzone: Number = 0
    left_trigger_deadzone: Number = 0
    right_trigger_deadzone: Number = 0
    gyroscope_threshold: int = 0
    orientation_threshold: int = 0
    accelerometer_threshold: int = 0


@dataclass
class ControllerInstanceData:
    controller: DualSenseController
    mocked_hidapi_device: MockedHidapiMockedHidapiDevice
