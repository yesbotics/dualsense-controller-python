from unittest.mock import MagicMock

import pytest as pytest

from dualsense_controller.api.DualSenseController import DualSenseController
from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.exception import InvalidDeviceIndexException
from tests.common import ControllerInstanceData


# # @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_enumerate_devices_mock,device_index,expect_is_raising_exception',
    [
        [0, None, True],
        [0, 0, True],
        [0, 1, True],
        [0, 999, True],
        [1, None, False],
        [1, 0, False],
        [1, 1, True],
        [1, 2, True],
        [1, 999, True],
        [2, None, False],
        [2, 0, False],
        [2, 1, False],
        [2, 2, True],
        [2, 3, True],
        [2, 999, True],
        [3, None, False],
        [3, 0, False],
        [3, 1, False],
        [3, 2, False],
        [3, 3, True],
        [3, 4, True],
        [4, 999, True],
    ],
    indirect=['fixture_enumerate_devices_mock']
)
def test_device_index(
        fixture_enumerate_devices_mock: MagicMock,
        device_index: int,
        expect_is_raising_exception: bool
) -> None:
    if expect_is_raising_exception:
        with pytest.raises(InvalidDeviceIndexException):
            DualSenseController(device_index)
    else:
        assert isinstance(DualSenseController(device_index), DualSenseController)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device',
    [
        ConnectionType.USB_01,
        ConnectionType.BT_31,
        ConnectionType.BT_01,
    ],
    indirect=['fixture_params_for_mocked_hidapi_device']
)
def test_instance(
        fixture_params_for_mocked_hidapi_device: ConnectionType,
        fixture_controller_instance: ControllerInstanceData
) -> None:
    assert isinstance(fixture_controller_instance.controller, DualSenseController)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,expected_conn_type',
    [
        [ConnectionType.USB_01, ConnectionType.USB_01],
        [ConnectionType.BT_31, ConnectionType.BT_31],
        [ConnectionType.BT_01, ConnectionType.BT_01],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device']
)
def test_instance_conntype(
        fixture_params_for_mocked_hidapi_device: ConnectionType,
        fixture_activated_instance: ControllerInstanceData,
        expected_conn_type: ConnectionType,
) -> None:
    assert isinstance(fixture_activated_instance.controller, DualSenseController)
    assert fixture_activated_instance.controller.is_active
    assert fixture_activated_instance.controller.connection_type.name == expected_conn_type.name
