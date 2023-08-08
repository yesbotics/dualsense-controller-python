from dataclasses import dataclass

from dualsense_controller import DualSenseController, Mapping, UpdateLevel
from tests.mock.HidapiDeviceMock import DeviceMock
from tests.mock.common import ConnTypeMock


@dataclass
class ControllerInstanceParams:
    conn_type_mock: ConnTypeMock = ConnTypeMock.USB_01
    mapping: Mapping = Mapping.DEFAULT
    update_level: UpdateLevel = UpdateLevel.DEFAULT


@dataclass
class ControllerInstanceData:
    controller: DualSenseController
    hidapi_device: DeviceMock
