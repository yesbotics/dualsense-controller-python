from dataclasses import dataclass

from dualsense_controller import DualSenseController, Mapping, UpdateLevel
from tests.mock.HidapiDeviceMock import MockedHidapiDevice


@dataclass
class ControllerInstanceParams:
    mapping: Mapping = Mapping.DEFAULT
    update_level: UpdateLevel = UpdateLevel.DEFAULT


@dataclass
class ControllerInstanceData:
    controller: DualSenseController
    mocked_hidapi_device: MockedHidapiDevice
