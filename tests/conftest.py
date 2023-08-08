from typing import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest as pytest
from _pytest.fixtures import SubRequest
from pytest_mock import MockerFixture

from dualsense_controller import DualSenseController
from tests.common import ControllerInstanceData, ControllerInstanceParams
from tests.mock.HidapiDeviceMock import DeviceMock
from tests.mock.common import DeviceInfoMock


@pytest.fixture
def fixture_device_info_mock() -> DeviceInfoMock:
    return DeviceInfoMock()


@pytest.fixture
def fixture_enumerate_devices_mock(
        request: SubRequest,
        fixture_device_info_mock: DeviceInfoMock
) -> Generator[MagicMock, None, None]:
    num_infos: int = request.param if hasattr(request, 'param') else 1
    with patch(
            "dualsense_controller.core.HidControllerDevice.HidControllerDevice.enumerate_devices",
            return_value=([fixture_device_info_mock] * num_infos) if num_infos > 0 else []
    ) as enumerate_devices_mock:
        yield enumerate_devices_mock


@pytest.fixture
def fixture_hidapi_device_mock(
        request: SubRequest,
        mocker: MockerFixture
) -> Generator[MagicMock, None, None]:
    device_mock: DeviceMock = DeviceMock(conn_type=request.param)
    create_mock: Mock = mocker.patch(
        'dualsense_controller.core.HidControllerDevice.HidControllerDevice._create'
    )
    create_mock.return_value = device_mock
    yield device_mock


@pytest.fixture
def fixture_controller_instance(
        request: SubRequest,
        fixture_enumerate_devices_mock: MagicMock,
        mocker: MockerFixture
) -> Generator[ControllerInstanceData, None, None]:
    params: ControllerInstanceParams = (
        request.param if hasattr(request, 'param') else ControllerInstanceParams()
    )
    device_mock: DeviceMock = DeviceMock(conn_type=params.conn_type_mock)
    create_mock: Mock = mocker.patch(
        'dualsense_controller.core.HidControllerDevice.HidControllerDevice._create'
    )
    create_mock.return_value = device_mock

    yield ControllerInstanceData(
        controller=DualSenseController(
            device_index_or_device_info=fixture_enumerate_devices_mock,
            mapping=params.mapping,
            update_level=params.update_level,
        ),
        hidapi_device=device_mock
    )


@pytest.fixture
def fixture_activated_instance(
        request: SubRequest,
        fixture_enumerate_devices_mock: MagicMock,
        mocker: MockerFixture
):
    params: ControllerInstanceParams = (
        request.param if hasattr(request, 'param') else ControllerInstanceParams()
    )

    device_mock: DeviceMock = DeviceMock(conn_type=params.conn_type_mock)
    create_mock: Mock = mocker.patch(
        'dualsense_controller.core.HidControllerDevice.HidControllerDevice._create'
    )
    create_mock.return_value = device_mock

    controller: DualSenseController = DualSenseController(
        device_index_or_device_info=fixture_enumerate_devices_mock,
        mapping=params.mapping,
        update_level=params.update_level,
    )
    controller.activate()
    yield ControllerInstanceData(
        controller=controller,
        hidapi_device=device_mock
    )
    controller.deactivate()
