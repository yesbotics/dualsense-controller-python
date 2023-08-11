from typing import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest as pytest
from _pytest.fixtures import SubRequest
from pytest_mock import MockerFixture

from dualsense_controller import DualSenseController
from tests.common import ControllerInstanceData, ControllerInstanceParams
from tests.mock.MockedHidapiMockedHidapiDevice import MockedHidapiMockedHidapiDevice
from tests.mock.common import DeviceInfoMock, ConnTypeMock


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
def fixture_params_for_mocked_hidapi_device(request: SubRequest) -> ConnTypeMock:
    return request.param if hasattr(request, 'param') else None


@pytest.fixture
def fixture_mocked_hidapi_device(
        fixture_params_for_mocked_hidapi_device,
        request: SubRequest,
        mocker: MockerFixture
) -> MockedHidapiMockedHidapiDevice:
    conn_type: ConnTypeMock = request.param if hasattr(request, 'param') else fixture_params_for_mocked_hidapi_device
    mocked_hidapi_device: MockedHidapiMockedHidapiDevice = MockedHidapiMockedHidapiDevice(conn_type=conn_type)
    create_mock: Mock = mocker.patch('dualsense_controller.core.HidControllerDevice.HidControllerDevice._create')
    create_mock.return_value = mocked_hidapi_device
    return mocked_hidapi_device


@pytest.fixture
def fixture_params_for_controller_instance(request: SubRequest) -> ControllerInstanceParams:
    return request.param if hasattr(request, 'param') else ControllerInstanceParams()


@pytest.fixture
def fixture_controller_instance(
        fixture_params_for_controller_instance: ControllerInstanceParams,
        request: SubRequest,
        fixture_enumerate_devices_mock: MagicMock,
        fixture_mocked_hidapi_device: MockedHidapiMockedHidapiDevice
) -> Generator[ControllerInstanceData, None, None]:
    # prepare
    params: ControllerInstanceParams = (
        request.param if hasattr(request, 'param') else fixture_params_for_controller_instance
    )
    # create
    yield ControllerInstanceData(
        controller=DualSenseController(
            device_index_or_device_info=fixture_enumerate_devices_mock,
            mapping=params.mapping,
            update_level=params.update_level,
        ),
        mocked_hidapi_device=fixture_mocked_hidapi_device
    )


@pytest.fixture
def fixture_activated_instance(
        request: SubRequest,
        fixture_controller_instance: ControllerInstanceData,
) -> Generator[ControllerInstanceData, None, None]:
    # activate
    fixture_controller_instance.controller.activate()
    # pass and do test stuff
    yield fixture_controller_instance
    # deactivate
    fixture_controller_instance.controller.deactivate()
