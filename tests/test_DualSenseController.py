from unittest.mock import MagicMock

import pytest as pytest

from dualsense_controller import ConnectionType, DualSenseController, InvalidDeviceIndexException, Mapping, Number
from tests.common import ControllerInstanceData, ControllerInstanceParams
from tests.mock.common import ConnTypeMock


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
    'fixture_controller_instance',
    [
        ControllerInstanceParams(ConnTypeMock.USB_01),
        ControllerInstanceParams(ConnTypeMock.BT_31),
    ],
    indirect=['fixture_controller_instance']
)
def test_instance(fixture_controller_instance: ControllerInstanceData) -> None:
    assert isinstance(fixture_controller_instance.controller, DualSenseController)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_controller_instance,expected_conn_type',
    [
        [ControllerInstanceParams(ConnTypeMock.USB_01), ConnectionType.USB_01],
        [ControllerInstanceParams(ConnTypeMock.BT_31), ConnectionType.BT_31],
    ],
    indirect=['fixture_controller_instance']
)
def test_instance_conntype(
        fixture_controller_instance: ControllerInstanceData,
        expected_conn_type: ConnectionType
) -> None:
    try:
        fixture_controller_instance.controller.activate()
        assert isinstance(fixture_controller_instance.controller, DualSenseController)
        assert fixture_controller_instance.controller.is_active
        assert fixture_controller_instance.controller.connection_type.name == expected_conn_type.name
    finally:
        fixture_controller_instance.controller.deactivate()


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_activated_instance,left_stick_y_raw,left_stick_y_mapped',
    [
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW), 0, 0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW), 127, 127],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW), 128, 128],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW), 255, 255],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW_INVERTED), 0, 255],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW_INVERTED), 127, 128],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW_INVERTED), 128, 127],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.RAW_INVERTED), 255, 0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT), 0, 127],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT), 127, 0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT), 128, -1],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT), 255, -128],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED), 0, -128],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED), 127, -1],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED), 128, 0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.DEFAULT_INVERTED), 255, 127],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED), 0, 1.0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED), 127, 0.0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED), 128, 0.0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED), 255, -1.0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED), 0, -1.0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED), 127, 0.0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED), 128, 0.0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.NORMALIZED_INVERTED), 255, 1.00],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.HUNDRED), 0, 100],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.HUNDRED), 127, 0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.HUNDRED), 128, 0],
        [ControllerInstanceParams(ConnTypeMock.USB_01, Mapping.HUNDRED), 255, -100],
    ],
    indirect=['fixture_activated_instance']
)
def test_mapping(
        fixture_activated_instance: ControllerInstanceData,
        left_stick_y_raw: int,
        left_stick_y_mapped: Number,
) -> None:
    fixture_activated_instance.hidapi_device.set_left_stick_y_byte(left_stick_y_raw)
    fixture_activated_instance.controller.wait_until_updated()
    assert isinstance(fixture_activated_instance.controller, DualSenseController)
    assert left_stick_y_mapped == pytest.approx(fixture_activated_instance.controller.left_stick_y.value, rel=1e-2)
