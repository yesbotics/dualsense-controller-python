import pytest as pytest

from dualsense_controller import DualSenseController, NoDeviceDetectedException, InvalidDeviceIndexException


def test_wrong_device_index():
    controller: DualSenseController = DualSenseController(999)
    with pytest.raises(InvalidDeviceIndexException):
        controller.init()
