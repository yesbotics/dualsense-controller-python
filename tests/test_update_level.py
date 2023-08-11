import pytest

from dualsense_controller import UpdateLevel
from tests.common import ControllerInstanceData, ControllerInstanceParams
from tests.mock.common import ConnTypeMock


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance',
    [
        [ConnTypeMock.USB_01, ControllerInstanceParams(update_level=UpdateLevel.DEFAULT)],
        [ConnTypeMock.BT_31, ControllerInstanceParams(update_level=UpdateLevel.DEFAULT)],
        # [ConnTypeMock.BT_01, ControllerInstanceParams(update_level=UpdateLevel.DEFAULT)],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device']
)
def test_update_level_default(
        fixture_params_for_mocked_hidapi_device: ConnTypeMock,
        fixture_params_for_controller_instance: ControllerInstanceData,
        fixture_controller_instance: ControllerInstanceData,
) -> None:
    def on_change():
        print('smaul')

    fixture_controller_instance.controller.btn_cross.on_change(on_change)
    fixture_controller_instance.controller.activate()
    # fixture_controller_instance.mocked_hidapi_device.set_btn_square(True)
    # fixture_controller_instance.mocked_hidapi_device.set_btn_cross(True)
    fixture_controller_instance.controller.wait_until_updated()

    assert fixture_controller_instance.controller.is_active
