import pytest

from dualsense_controller import UpdateLevel
from tests.common import ControllerInstanceData, ControllerInstanceParams

# # @pytest.mark.skip(reason="temp disabled")
# @pytest.mark.parametrize(
#     'fixture_params_for_mocked_hidapi_device',
#     [
#         [ConnectionType.USB_01],
#         [ConnectionType.BT_31],
#         [ConnectionType.BT_01],
#     ],
#     indirect=['fixture_params_for_mocked_hidapi_device']
# )
# def test_update_level_haengbliem(
#         fixture_params_for_mocked_hidapi_device: ConnectionType,
#         fixture_params_for_controller_instance: ControllerInstanceData,
#         fixture_activated_instance: ControllerInstanceData,
# ) -> None:
#     fixture_activated_instance.controller.btn_cross.on_change(lambda _: _)
#     fixture_activated_instance.mocked_hidapi_device.set_btn_square(True)
#     fixture_activated_instance.mocked_hidapi_device.set_btn_cross(True)
#     fixture_activated_instance.controller.wait_until_updated()
#
#     assert fixture_activated_instance.controller.btn_cross.pressed is True
#     assert fixture_activated_instance.controller.btn_square.pressed is None
