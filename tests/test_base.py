import pytest as pytest

from dualsense_controller import DualSenseController

from dualsense_controller.exceptions import InvalidDeviceIndexException


def test_wrong_device_index():
    controller: DualSenseController = DualSenseController(999)
    with pytest.raises(InvalidDeviceIndexException):
        controller.init()
