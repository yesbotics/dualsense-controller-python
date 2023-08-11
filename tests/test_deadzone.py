from typing import Final
from unittest.mock import MagicMock

import pytest

from dualsense_controller import ConnectionType, DualSenseController, JoyStick, Mapping, Number, UpdateLevel
from tests.common import ControllerInstanceData, ControllerInstanceParams


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'deadzone,expect_raise_value_error', [
        [-1, True],
        [0, False],
        [1, False],
        [-0.0000000000000001, True],
        [0.0000000000000001, False],
    ]
)
def test_deadzone_invalid_negative(
        fixture_enumerate_devices_mock: MagicMock,
        deadzone: Number,
        expect_raise_value_error: bool
) -> None:
    ERRMSG: Final[str] = 'Deadzone value must not be negative'

    if expect_raise_value_error:
        with pytest.raises(ValueError) as err:
            DualSenseController(left_joystick_deadzone=deadzone)
            DualSenseController(right_joystick_deadzone=deadzone)
            DualSenseController(left_trigger_deadzone=deadzone)
            DualSenseController(right_trigger_deadzone=deadzone)

        assert err.value.args[0] == ERRMSG
    else:
        assert isinstance(DualSenseController(left_joystick_deadzone=deadzone), DualSenseController)
        assert isinstance(DualSenseController(right_joystick_deadzone=deadzone), DualSenseController)
        assert isinstance(DualSenseController(left_trigger_deadzone=deadzone), DualSenseController)
        assert isinstance(DualSenseController(right_trigger_deadzone=deadzone), DualSenseController)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'mapping,joystick_deadzone,trigger_deadzone,expect_warning', [
        [Mapping.RAW, 0, 0, False],
        [Mapping.RAW, 11, 0, False],
        [Mapping.RAW, 127, 0, False],
        [Mapping.RAW, 127.49999999999999, 0, False],
        [Mapping.RAW, 127.5, 0, True],
        [Mapping.RAW, 128, 0, True],
        [Mapping.RAW, 0, 11, False],
        [Mapping.RAW, 0, 127, False],
        [Mapping.RAW, 0, 127.5, False],
        [Mapping.RAW, 0, 128, False],
        [Mapping.RAW, 0, 254, False],
        [Mapping.RAW, 0, 255, True],
        [Mapping.RAW_INVERTED, 0, 0, False],
        [Mapping.RAW_INVERTED, 11, 0, False],
        [Mapping.RAW_INVERTED, 127, 0, False],
        [Mapping.RAW_INVERTED, 127.49999999999999, 0, False],
        [Mapping.RAW_INVERTED, 127.5, 0, True],
        [Mapping.RAW_INVERTED, 128, 0, True],
        [Mapping.RAW_INVERTED, 0, 127, False],
        [Mapping.RAW_INVERTED, 0, 127.5, False],
        [Mapping.RAW_INVERTED, 0, 128, False],
        [Mapping.RAW_INVERTED, 0, 254, False],
        [Mapping.RAW_INVERTED, 0, 255, True],
        [Mapping.NORMALIZED, 0, 0, False],
        [Mapping.NORMALIZED, 0.11, 0, False],
        [Mapping.NORMALIZED, 0.999999999999, 0, False],
        [Mapping.NORMALIZED, 1, 0, True],
        [Mapping.NORMALIZED, 11, 0, True],
        [Mapping.NORMALIZED, 0, 0, False],
        [Mapping.NORMALIZED, 0, 0.999999999999, False],
        [Mapping.NORMALIZED, 0, 1, True],
        [Mapping.NORMALIZED, 0, 11, True],
        [Mapping.NORMALIZED_INVERTED, 0, 0, False],
        [Mapping.NORMALIZED_INVERTED, 0.11, 0, False],
        [Mapping.NORMALIZED_INVERTED, 0.999999999999, 0, False],
        [Mapping.NORMALIZED_INVERTED, 1, 0, True],
        [Mapping.NORMALIZED_INVERTED, 11, 0, True],
        [Mapping.NORMALIZED_INVERTED, 0, 0, False],
        [Mapping.NORMALIZED_INVERTED, 0, 0.999999999999, False],
        [Mapping.NORMALIZED_INVERTED, 0, 1, True],
        [Mapping.NORMALIZED_INVERTED, 0, 11, True],
        [Mapping.DEFAULT, 0, 0, False],
        [Mapping.DEFAULT, 11, 0, False],
        [Mapping.DEFAULT, 127, 0, False],
        [Mapping.DEFAULT, 127.49999999999999, 0, False],
        [Mapping.DEFAULT, 127.5, 0, True],
        [Mapping.DEFAULT, 128, 0, True],
        [Mapping.DEFAULT, 255, 0, True],
        [Mapping.DEFAULT, 0, 0, False],
        [Mapping.DEFAULT, 0, 11, False],
        [Mapping.DEFAULT, 0, 254, False],
        [Mapping.DEFAULT, 0, 254.9999999999, False],
        [Mapping.DEFAULT, 0, 255, True],
        [Mapping.DEFAULT, 0, 512, True],
        [Mapping.DEFAULT_INVERTED, 0, 0, False],
        [Mapping.DEFAULT_INVERTED, 11, 0, False],
        [Mapping.DEFAULT_INVERTED, 127, 0, False],
        [Mapping.DEFAULT_INVERTED, 127.49999999999999, 0, False],
        [Mapping.DEFAULT_INVERTED, 127.5, 0, True],
        [Mapping.DEFAULT_INVERTED, 128, 0, True],
        [Mapping.DEFAULT_INVERTED, 255, 0, True],
        [Mapping.DEFAULT_INVERTED, 0, 0, False],
        [Mapping.DEFAULT_INVERTED, 0, 11, False],
        [Mapping.DEFAULT_INVERTED, 0, 254, False],
        [Mapping.DEFAULT_INVERTED, 0, 254.9999999999, False],
        [Mapping.DEFAULT_INVERTED, 0, 255, True],
        [Mapping.DEFAULT_INVERTED, 0, 512, True],
        [Mapping.HUNDRED, 0, 0, False],
        [Mapping.HUNDRED, 11, 0, False],
        [Mapping.HUNDRED, 99, 0, False],
        [Mapping.HUNDRED, 99.9999999999999, 0, False],
        [Mapping.HUNDRED, 100, 0, True],
        [Mapping.HUNDRED, 200, 0, True],
        [Mapping.HUNDRED, 0, 0, False],
        [Mapping.HUNDRED, 0, 11, False],
        [Mapping.HUNDRED, 0, 99, False],
        [Mapping.HUNDRED, 0, 99.9999999999999, False],
        [Mapping.HUNDRED, 0, 100, True],
        [Mapping.HUNDRED, 0, 200, True],
    ]
)
def test_deadzone_warning_to_big(
        fixture_enumerate_devices_mock: MagicMock,
        mapping: Mapping,
        joystick_deadzone: Number,
        trigger_deadzone: Number,
        expect_warning: bool
) -> None:
    if expect_warning:
        WARNMSG: Final[str] = "is very big related to chosen mapping"
        with pytest.warns(UserWarning, match=WARNMSG):
            DualSenseController(mapping=mapping, left_joystick_deadzone=joystick_deadzone)
            DualSenseController(mapping=mapping, right_joystick_deadzone=joystick_deadzone)
            DualSenseController(mapping=mapping, left_trigger_deadzone=trigger_deadzone)
            DualSenseController(mapping=mapping, right_trigger_deadzone=trigger_deadzone)
    else:
        with pytest.warns(None) as record:
            DualSenseController(mapping=mapping, left_joystick_deadzone=joystick_deadzone)
            DualSenseController(mapping=mapping, right_joystick_deadzone=joystick_deadzone)
            DualSenseController(mapping=mapping, left_trigger_deadzone=trigger_deadzone)
            DualSenseController(mapping=mapping, right_trigger_deadzone=trigger_deadzone)
        assert len(record) == 0


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance'
    ',left_stick,expected_left_stick'
    ',right_stick,expected_right_stick'
    ',left_trigger,expected_left_trigger'
    ',right_trigger,expected_right_trigger'
    , [
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            0, 0, 0, 0, 0, 0, 0, 0
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            0, 0, 0, 0, 30, 0, 30, 0
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            0, 0, 0, 0, 31, 31, 31, 31
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            0, 0, 0, 0, 255, 255, 255, 255
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            106, 106, 106, 106, 0, 0, 0, 0
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            107, 127.5, 107, 127.5, 0, 0, 0, 0
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            147, 127.5, 147, 127.5, 0, 0, 0, 0
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            149, 149, 149, 149, 0, 0, 0, 0
        ],
        [
            ConnectionType.USB_01,
            ControllerInstanceParams(
                mapping=Mapping.RAW,
                update_level=UpdateLevel.PAINSTAKING,
                left_joystick_deadzone=30,
                right_joystick_deadzone=30,
                left_trigger_deadzone=30,
                right_trigger_deadzone=30,
            ),
            255, 255, 255, 255, 0, 0, 0, 0
        ],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device', 'fixture_params_for_controller_instance']
)
def test_apply_deadzone(
        fixture_params_for_mocked_hidapi_device: ConnectionType,
        fixture_params_for_controller_instance: ControllerInstanceData,
        fixture_activated_instance: ControllerInstanceData,
        left_stick: int,
        expected_left_stick: int,
        right_stick: int,
        expected_right_stick: int,
        left_trigger: int,
        expected_left_trigger: int,
        right_trigger: int,
        expected_right_trigger: int,
) -> None:
    fixture_activated_instance.mocked_hidapi_device.set_left_stick_raw(JoyStick(left_stick, left_stick))
    fixture_activated_instance.mocked_hidapi_device.set_right_stick_raw(JoyStick(right_stick, right_stick))
    fixture_activated_instance.mocked_hidapi_device.set_left_trigger_raw(left_trigger)
    fixture_activated_instance.mocked_hidapi_device.set_right_trigger_raw(right_trigger)
    fixture_activated_instance.controller.wait_until_updated()
    assert fixture_activated_instance.controller.left_stick.value.x == expected_left_stick
    assert fixture_activated_instance.controller.left_stick_x.value == expected_left_stick
    assert fixture_activated_instance.controller.left_stick.value.y == expected_left_stick
    assert fixture_activated_instance.controller.left_stick_y.value == expected_left_stick
    assert fixture_activated_instance.controller.right_stick.value.x == expected_right_stick
    assert fixture_activated_instance.controller.right_stick_x.value == expected_right_stick
    assert fixture_activated_instance.controller.right_stick.value.y == expected_right_stick
    assert fixture_activated_instance.controller.right_stick_y.value == expected_right_stick
    assert fixture_activated_instance.controller.left_trigger.value == expected_left_trigger
    assert fixture_activated_instance.controller.right_trigger.value == expected_right_trigger
