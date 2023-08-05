from typing import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest as pytest
from _pytest.fixtures import SubRequest
from pytest_mock import MockerFixture

from dualsense_controller import ConnectionType, DualSenseController, InvalidDeviceIndexException, Mapping, UpdateLevel
from tests.mock import ConnTypeMock, DeviceInfoMock, DeviceMock


@pytest.fixture
def fixture_device_info_mock() -> DeviceInfoMock:
    return DeviceInfoMock()


@pytest.fixture
def fixture_enumerate_devices_mock(fixture_device_info_mock: DeviceInfoMock) -> Generator[MagicMock, None, None]:
    with patch(
            "dualsense_controller.core.HidControllerDevice.HidControllerDevice.enumerate_devices",
            return_value=[fixture_device_info_mock]
    ) as enumerate_devices_mock:
        yield enumerate_devices_mock


@pytest.fixture
def fixture_controller_instance(
        request: SubRequest,
        fixture_enumerate_devices_mock: MagicMock,
        mocker: MockerFixture
) -> DualSenseController:
    param_conn_type: ConnTypeMock = request.param[0] if len(request.param) >= 1 else ConnTypeMock.USB_01
    param_mapping: Mapping = request.param[1] if len(request.param) >= 2 else Mapping.DEFAULT
    param_update_level: UpdateLevel = request.param[2] if len(request.param) >= 3 else UpdateLevel.DEFAULT

    device_mock: DeviceMock = DeviceMock(conn_type=param_conn_type)
    create_mock: Mock = mocker.patch(
        'dualsense_controller.core.HidControllerDevice.HidControllerDevice._create'
    )
    create_mock.return_value = device_mock

    return DualSenseController(
        device_index_or_device_info=fixture_enumerate_devices_mock,
        mapping=param_mapping,
        update_level=param_update_level,
    )


def test_wrong_device_index(fixture_enumerate_devices_mock: MagicMock) -> None:
    with pytest.raises(InvalidDeviceIndexException):
        DualSenseController(device_index_or_device_info=99999999)


@pytest.mark.parametrize(
    'fixture_controller_instance',
    [
        [[ConnTypeMock.USB_01]],
        [[ConnTypeMock.BT_31]],
    ],
    indirect=['fixture_controller_instance']
)
def test_controller_instance(fixture_controller_instance: DualSenseController) -> None:
    assert isinstance(fixture_controller_instance, DualSenseController)


@pytest.mark.parametrize(
    'fixture_controller_instance,expected_conn_type',
    [
        [[ConnTypeMock.USB_01], ConnectionType.USB_01],
        [[ConnTypeMock.BT_31], ConnectionType.BT_31],
    ],
    indirect=['fixture_controller_instance']
)
def test_controller_instance_activate(
        fixture_controller_instance: DualSenseController,
        expected_conn_type: ConnectionType
) -> None:
    fixture_controller_instance.activate()
    assert isinstance(fixture_controller_instance, DualSenseController)
    assert fixture_controller_instance.is_active
    assert fixture_controller_instance.connection_type.name == expected_conn_type.name

# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_controller_instance',
    [
        [[ConnTypeMock.USB_01, Mapping.RAW]],
        [[ConnTypeMock.USB_01, Mapping.RAW_INVERTED]],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT]],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED]],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED]],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED]],
        [[ConnTypeMock.USB_01, Mapping.HUNDRED]],
    ],
    indirect=['fixture_controller_instance']
)
def test_controller_instance_mapping(fixture_controller_instance: DualSenseController) -> None:
    assert isinstance(fixture_controller_instance, DualSenseController)
    # fixture_controller_instance.activate()
