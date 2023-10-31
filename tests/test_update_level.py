import pytest

from dualsense_controller.api.enum import UpdateLevel
from dualsense_controller.core.enum import ConnectionType
from tests.common import ControllerInstanceData, ControllerInstanceParams


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance',
    [
        [ConnectionType.USB_01, ControllerInstanceParams(update_level=UpdateLevel.HAENGBLIEM)],
        [ConnectionType.BT_31, ControllerInstanceParams(update_level=UpdateLevel.HAENGBLIEM)],
        [ConnectionType.BT_01, ControllerInstanceParams(update_level=UpdateLevel.HAENGBLIEM)],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device']
)
def test_update_level_haengbliem(
        fixture_params_for_mocked_hidapi_device: ConnectionType,
        fixture_params_for_controller_instance: ControllerInstanceData,
        fixture_activated_instance: ControllerInstanceData,
) -> None:
    fixture_activated_instance.controller.btn_cross.on_change(lambda _: _)
    fixture_activated_instance.mocked_hidapi_device.set_btn_square(True)
    fixture_activated_instance.mocked_hidapi_device.set_btn_cross(True)
    fixture_activated_instance.controller.wait_until_updated()

    assert fixture_activated_instance.controller.btn_cross.pressed is True
    assert fixture_activated_instance.controller.btn_square.pressed is None


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance',
    [
        [ConnectionType.USB_01, ControllerInstanceParams(update_level=UpdateLevel.PAINSTAKING)],
        [ConnectionType.BT_31, ControllerInstanceParams(update_level=UpdateLevel.PAINSTAKING)],
        [ConnectionType.BT_01, ControllerInstanceParams(update_level=UpdateLevel.PAINSTAKING)],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device']
)
def test_update_level_painstaking(
        fixture_params_for_mocked_hidapi_device: ConnectionType,
        fixture_params_for_controller_instance: ControllerInstanceData,
        fixture_activated_instance: ControllerInstanceData,
) -> None:
    fixture_activated_instance.mocked_hidapi_device.set_btn_square(True)
    fixture_activated_instance.mocked_hidapi_device.set_btn_cross(True)
    fixture_activated_instance.controller.wait_until_updated()

    assert fixture_activated_instance.controller.btn_cross.pressed is True
    assert fixture_activated_instance.controller.btn_square.pressed is True


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance',
    [
        [ConnectionType.USB_01, ControllerInstanceParams(update_level=UpdateLevel.DEFAULT)],
        [ConnectionType.BT_31, ControllerInstanceParams(update_level=UpdateLevel.DEFAULT)],
        [ConnectionType.BT_01, ControllerInstanceParams(update_level=UpdateLevel.DEFAULT)],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device']
)
def test_update_level_default(
        fixture_params_for_mocked_hidapi_device: ConnectionType,
        fixture_params_for_controller_instance: ControllerInstanceData,
        fixture_activated_instance: ControllerInstanceData,
) -> None:
    fixture_activated_instance.mocked_hidapi_device.set_btn_square(True)
    fixture_activated_instance.mocked_hidapi_device.set_btn_cross(True)
    fixture_activated_instance.controller.wait_until_updated()

    assert fixture_activated_instance.controller.btn_cross.pressed is True
    assert fixture_activated_instance.controller.btn_square.pressed is True
