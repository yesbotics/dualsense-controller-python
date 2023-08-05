import time
from dataclasses import dataclass
from typing import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest as pytest
from _pytest.fixtures import SubRequest
from pytest_mock import MockerFixture

from dualsense_controller import ConnectionType, DualSenseController, InvalidDeviceIndexException, Mapping, Number, \
    UpdateLevel
from tests.mock import ConnTypeMock, DeviceInfoMock, DeviceMock


@dataclass
class ControllerInstanceData:
    controller: DualSenseController
    device: DeviceMock


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
) -> ControllerInstanceData:
    param_conn_type: ConnTypeMock = request.param[0] if len(request.param) >= 1 else ConnTypeMock.USB_01
    param_mapping: Mapping = request.param[1] if len(request.param) >= 2 else Mapping.DEFAULT
    param_update_level: UpdateLevel = request.param[2] if len(request.param) >= 3 else UpdateLevel.DEFAULT

    device_mock: DeviceMock = DeviceMock(conn_type=param_conn_type)
    create_mock: Mock = mocker.patch(
        'dualsense_controller.core.HidControllerDevice.HidControllerDevice._create'
    )
    create_mock.return_value = device_mock

    return ControllerInstanceData(
        controller=DualSenseController(
            device_index_or_device_info=fixture_enumerate_devices_mock,
            mapping=param_mapping,
            update_level=param_update_level,
        ),
        device=device_mock
    )


# @pytest.mark.skip(reason="temp disabled")
def test_wrong_device_index(fixture_enumerate_devices_mock: MagicMock) -> None:
    with pytest.raises(InvalidDeviceIndexException):
        DualSenseController(device_index_or_device_info=99999999)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_controller_instance',
    [
        [ConnTypeMock.USB_01],
        [ConnTypeMock.BT_31],
    ],
    indirect=['fixture_controller_instance']
)
def test_controller_instance(fixture_controller_instance: ControllerInstanceData) -> None:
    assert isinstance(fixture_controller_instance.controller, DualSenseController)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_controller_instance,expected_conn_type',
    [
        [[ConnTypeMock.USB_01], ConnectionType.USB_01],
        [[ConnTypeMock.BT_31], ConnectionType.BT_31],
    ],
    indirect=['fixture_controller_instance']
)
def test_controller_instance_activate(
        fixture_controller_instance: ControllerInstanceData,
        expected_conn_type: ConnectionType
) -> None:
    fixture_controller_instance.controller.activate()
    assert isinstance(fixture_controller_instance.controller, DualSenseController)
    assert fixture_controller_instance.controller.is_active
    assert fixture_controller_instance.controller.connection_type.name == expected_conn_type.name


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_controller_instance,left_stick_y_raw,left_stick_y_mapped',
    [
        [[ConnTypeMock.USB_01, Mapping.RAW], 0, 0],
        [[ConnTypeMock.USB_01, Mapping.RAW], 127, 127],
        [[ConnTypeMock.USB_01, Mapping.RAW], 128, 128],
        [[ConnTypeMock.USB_01, Mapping.RAW], 255, 255],
        [[ConnTypeMock.USB_01, Mapping.RAW_INVERTED], 0, 255],
        [[ConnTypeMock.USB_01, Mapping.RAW_INVERTED], 127, 128],
        [[ConnTypeMock.USB_01, Mapping.RAW_INVERTED], 128, 127],
        [[ConnTypeMock.USB_01, Mapping.RAW_INVERTED], 255, 0],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT], 0, 127],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT], 127, 0],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT], 128, -1],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT], 255, -128],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED], 0, -128],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED], 127, -1],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED], 128, 0],
        [[ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED], 255, 127],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED], 0, 1.0],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED], 127, 0.0],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED], 128, 0.0],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED], 255, -1.0],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED], 0, -1.0],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED], 127, 0.0],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED], 128, 0.0],
        [[ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED], 255, 1.00],
        [[ConnTypeMock.USB_01, Mapping.HUNDRED], 0, 100],
        [[ConnTypeMock.USB_01, Mapping.HUNDRED], 127, 0],
        [[ConnTypeMock.USB_01, Mapping.HUNDRED], 128, 0],
        [[ConnTypeMock.USB_01, Mapping.HUNDRED], 255, -100],
    ],
    indirect=['fixture_controller_instance']
)
def test_controller_instance_mapping(
        fixture_controller_instance: ControllerInstanceData,
        left_stick_y_raw: int,
        left_stick_y_mapped: Number,
) -> None:
    fixture_controller_instance.controller.activate()
    fixture_controller_instance.device.set_left_stick_y_byte(left_stick_y_raw)
    # while not fixture_controller_instance.controller.left_stick_y.changed:
    #     time.sleep(0.1)

    assert isinstance(fixture_controller_instance.controller, DualSenseController)
    assert left_stick_y_mapped == pytest.approx(fixture_controller_instance.controller.left_stick_y.value, rel=1e-2)
