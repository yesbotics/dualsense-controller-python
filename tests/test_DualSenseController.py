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
def device_info_mock() -> DeviceInfoMock:
    return DeviceInfoMock()


@pytest.fixture
def enumerate_devices_mock(
        request: SubRequest,
        device_info_mock: DeviceInfoMock
) -> Generator[MagicMock, None, None]:
    num_infos: int = request.param if hasattr(request, 'param') else 1
    with patch(
            "dualsense_controller.core.HidControllerDevice.HidControllerDevice.enumerate_devices",
            return_value=([device_info_mock] * num_infos) if num_infos > 0 else []
    ) as enumerate_devices_mock:
        yield enumerate_devices_mock


@pytest.fixture
def controller_instance(
        request: SubRequest,
        enumerate_devices_mock: MagicMock,
        mocker: MockerFixture
) -> Generator[ControllerInstanceData, None, None]:
    params: tuple[ConnTypeMock, Mapping, UpdateLevel] = request.param if hasattr(request, 'param') else ()
    param_conn_type: ConnTypeMock = params[0] if len(params) >= 1 else ConnTypeMock.USB_01
    param_mapping: Mapping = params[1] if len(params) >= 2 else Mapping.DEFAULT
    param_update_level: UpdateLevel = params[2] if len(params) >= 3 else UpdateLevel.DEFAULT

    device_mock: DeviceMock = DeviceMock(conn_type=param_conn_type)
    create_mock: Mock = mocker.patch(
        'dualsense_controller.core.HidControllerDevice.HidControllerDevice._create'
    )
    create_mock.return_value = device_mock

    yield ControllerInstanceData(
        controller=DualSenseController(
            device_index_or_device_info=enumerate_devices_mock,
            mapping=param_mapping,
            update_level=param_update_level,
        ),
        device=device_mock
    )


@pytest.fixture
def activated_instance(
        request: SubRequest,
        enumerate_devices_mock: MagicMock,
        mocker: MockerFixture
):
    params: tuple[ConnTypeMock, Mapping, UpdateLevel] = request.param if hasattr(request, 'param') else ()
    param_conn_type: ConnTypeMock = params[0] if len(params) >= 1 else ConnTypeMock.USB_01
    param_mapping: Mapping = params[1] if len(params) >= 2 else Mapping.DEFAULT
    param_update_level: UpdateLevel = params[2] if len(params) >= 3 else UpdateLevel.DEFAULT

    device_mock: DeviceMock = DeviceMock(conn_type=param_conn_type)
    create_mock: Mock = mocker.patch(
        'dualsense_controller.core.HidControllerDevice.HidControllerDevice._create'
    )
    create_mock.return_value = device_mock

    controller: DualSenseController = DualSenseController(
        device_index_or_device_info=enumerate_devices_mock,
        mapping=param_mapping,
        update_level=param_update_level,
    )
    controller.activate()
    yield ControllerInstanceData(
        controller=controller,
        device=device_mock
    )
    controller.deactivate()


# # @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'enumerate_devices_mock,device_index,expect_is_raising_exception',
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
    indirect=['enumerate_devices_mock']
)
def test_device_index(
        enumerate_devices_mock: MagicMock,
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
    'controller_instance',
    [
        [ConnTypeMock.USB_01],
        [ConnTypeMock.BT_31],
    ],
    indirect=['controller_instance']
)
def test_instance(controller_instance: ControllerInstanceData) -> None:
    assert isinstance(controller_instance.controller, DualSenseController)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'controller_instance,expected_conn_type',
    [
        [[ConnTypeMock.USB_01], ConnectionType.USB_01],
        [[ConnTypeMock.BT_31], ConnectionType.BT_31],
    ],
    indirect=['controller_instance']
)
def test_instance_conntype(
        controller_instance: ControllerInstanceData,
        expected_conn_type: ConnectionType
) -> None:
    try:
        controller_instance.controller.activate()
        assert isinstance(controller_instance.controller, DualSenseController)
        assert controller_instance.controller.is_active
        assert controller_instance.controller.connection_type.name == expected_conn_type.name
    finally:
        controller_instance.controller.deactivate()


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'activated_instance,left_stick_y_raw,left_stick_y_mapped',
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
    indirect=['activated_instance']
)
def test_mapping(
        activated_instance: ControllerInstanceData,
        left_stick_y_raw: int,
        left_stick_y_mapped: Number,
) -> None:
    activated_instance.device.set_left_stick_y_byte(left_stick_y_raw)
    activated_instance.controller.wait_until_updated()
    assert isinstance(activated_instance.controller, DualSenseController)
    assert left_stick_y_mapped == pytest.approx(activated_instance.controller.left_stick_y.value, rel=1e-2)
