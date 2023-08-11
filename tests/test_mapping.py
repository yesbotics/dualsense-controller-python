import pytest as pytest

from dualsense_controller import DualSenseController, Mapping, Number
from tests.common import ControllerInstanceData, ControllerInstanceParams
from tests.mock.common import ConnTypeMock


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance'
    ',left_stick_x_raw,left_stick_x_mapped'
    ',left_stick_y_raw,left_stick_y_mapped'
    ',right_stick_x_raw,right_stick_x_mapped'
    ',right_stick_y_raw,right_stick_y_mapped'
    ',left_trigger_raw,left_trigger_mapped'
    ',right_trigger_raw,right_trigger_mapped'
    , [
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW),
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW),
         127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW),
         128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW),
         255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         127, 127, 127, 128, 127, 127, 127, 128, 127, 127, 127, 127],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         128, 128, 128, 127, 128, 128, 128, 127, 128, 128, 128, 128],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT),
         0, -128, 0, 127, 0, -128, 0, 127, 0, 0, 0, 0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT),
         127, -1, 127, 0, 127, -1, 127, 0, 127, 127, 127, 127],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT),
         128, 0, 128, -1, 128, 0, 128, -1, 128, 128, 128, 128],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT),
         255, 127, 255, -128, 255, 127, 255, -128, 255, 255, 255, 255],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         0, -128, 0, -128, 0, -128, 0, -128, 0, 0, 0, 0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         127, -1, 127, -1, 127, -1, 127, -1, 127, 127, 127, 127],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         128, 0, 128, 0, 128, 0, 128, 0, 128, 128, 128, 128],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         255, 127, 255, 127, 255, 127, 255, 127, 255, 255, 255, 255],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED),
         0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, 0.0, 0, 0.0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED),
         127, 0.0, 127, 0.0, 127, 0.0, 127, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED),
         128, 0.0, 128, 0.0, 128, 0.0, 128, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED),
         255, 1.0, 255, -1.0, 255, 1.0, 255, -1.0, 255, 1.0, 255, 1.0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         0, -1.0, 0, -1.0, 0, -1.0, 0, -1.0, 0, 0.0, 0, 0.0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         127, 0.0, 127, 0.0, 127, 0.0, 127, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         128, 0.0, 128, 0.0, 128, 0.0, 128, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         255, 1.00, 255, 1.00, 255, 1.00, 255, 1.00, 255, 1.0, 255, 1.0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.HUNDRED),
         0, -100, 0, 100, 0, -100, 0, 100, 0, 0, 0, 0],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.HUNDRED),
         127, 0, 127, 0, 127, 0, 127, 0, 127, 49, 127, 49],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.HUNDRED),
         128, 0, 128, 0, 128, 0, 128, 0, 128, 50, 128, 50],
        [ConnTypeMock.USB_01, ControllerInstanceParams(Mapping.HUNDRED),
         255, 100, 255, -100, 255, 100, 255, -100, 255, 100, 255, 100],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device', 'fixture_params_for_controller_instance']
)
def test_mapping_usb01(
        fixture_params_for_mocked_hidapi_device: ConnTypeMock,
        fixture_params_for_controller_instance: ControllerInstanceParams,
        fixture_activated_instance: ControllerInstanceData,
        left_stick_x_raw: int,
        left_stick_x_mapped: Number,
        left_stick_y_raw: int,
        left_stick_y_mapped: Number,
        right_stick_x_raw: int,
        right_stick_x_mapped: Number,
        right_stick_y_raw: int,
        right_stick_y_mapped: Number,
        left_trigger_raw: int,
        left_trigger_mapped: Number,
        right_trigger_raw: int,
        right_trigger_mapped: Number,
) -> None:
    fixture_activated_instance.mocked_hidapi_device.set_left_stick_x_raw(left_stick_x_raw)
    fixture_activated_instance.mocked_hidapi_device.set_left_stick_y_raw(left_stick_y_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_stick_x_raw(right_stick_x_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_stick_y_raw(right_stick_y_raw)
    fixture_activated_instance.mocked_hidapi_device.set_left_trigger_raw(left_trigger_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_trigger_raw(right_trigger_raw)
    fixture_activated_instance.controller.wait_until_updated()
    assert left_stick_x_mapped == pytest.approx(fixture_activated_instance.controller.left_stick_x.value, rel=1e-4)
    assert left_stick_y_mapped == pytest.approx(fixture_activated_instance.controller.left_stick_y.value, rel=1e-4)
    assert right_stick_x_mapped == pytest.approx(fixture_activated_instance.controller.right_stick_x.value, rel=1e-4)
    assert right_stick_y_mapped == pytest.approx(fixture_activated_instance.controller.right_stick_y.value, rel=1e-4)
    assert left_trigger_mapped == pytest.approx(fixture_activated_instance.controller.left_trigger.value, rel=1e-4)
    assert right_trigger_mapped == pytest.approx(fixture_activated_instance.controller.right_trigger.value, rel=1e-4)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance'
    ',left_stick_x_raw,left_stick_x_mapped'
    ',left_stick_y_raw,left_stick_y_mapped'
    ',right_stick_x_raw,right_stick_x_mapped'
    ',right_stick_y_raw,right_stick_y_mapped'
    ',left_trigger_raw,left_trigger_mapped'
    ',right_trigger_raw,right_trigger_mapped'
    , [
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW),
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW),
         127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW),
         128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW),
         255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW_INVERTED),
         0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW_INVERTED),
         127, 127, 127, 128, 127, 127, 127, 128, 127, 127, 127, 127],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW_INVERTED),
         128, 128, 128, 127, 128, 128, 128, 127, 128, 128, 128, 128],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.RAW_INVERTED),
         255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT),
         0, -128, 0, 127, 0, -128, 0, 127, 0, 0, 0, 0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT),
         127, -1, 127, 0, 127, -1, 127, 0, 127, 127, 127, 127],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT),
         128, 0, 128, -1, 128, 0, 128, -1, 128, 128, 128, 128],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT),
         255, 127, 255, -128, 255, 127, 255, -128, 255, 255, 255, 255],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         0, -128, 0, -128, 0, -128, 0, -128, 0, 0, 0, 0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         127, -1, 127, -1, 127, -1, 127, -1, 127, 127, 127, 127],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         128, 0, 128, 0, 128, 0, 128, 0, 128, 128, 128, 128],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         255, 127, 255, 127, 255, 127, 255, 127, 255, 255, 255, 255],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED),
         0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, 0.0, 0, 0.0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED),
         127, 0.0, 127, 0.0, 127, 0.0, 127, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED),
         128, 0.0, 128, 0.0, 128, 0.0, 128, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED),
         255, 1.0, 255, -1.0, 255, 1.0, 255, -1.0, 255, 1.0, 255, 1.0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         0, -1.0, 0, -1.0, 0, -1.0, 0, -1.0, 0, 0.0, 0, 0.0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         127, 0.0, 127, 0.0, 127, 0.0, 127, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         128, 0.0, 128, 0.0, 128, 0.0, 128, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         255, 1.00, 255, 1.00, 255, 1.00, 255, 1.00, 255, 1.0, 255, 1.0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.HUNDRED),
         0, -100, 0, 100, 0, -100, 0, 100, 0, 0, 0, 0],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.HUNDRED),
         127, 0, 127, 0, 127, 0, 127, 0, 127, 49, 127, 49],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.HUNDRED),
         128, 0, 128, 0, 128, 0, 128, 0, 128, 50, 128, 50],
        [ConnTypeMock.BT_31, ControllerInstanceParams(Mapping.HUNDRED),
         255, 100, 255, -100, 255, 100, 255, -100, 255, 100, 255, 100],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device', 'fixture_params_for_controller_instance']
)
def test_mapping_bt31(
        fixture_params_for_mocked_hidapi_device: ConnTypeMock,
        fixture_params_for_controller_instance: ControllerInstanceParams,
        fixture_activated_instance: ControllerInstanceData,
        left_stick_x_raw: int,
        left_stick_x_mapped: Number,
        left_stick_y_raw: int,
        left_stick_y_mapped: Number,
        right_stick_x_raw: int,
        right_stick_x_mapped: Number,
        right_stick_y_raw: int,
        right_stick_y_mapped: Number,
        left_trigger_raw: int,
        left_trigger_mapped: Number,
        right_trigger_raw: int,
        right_trigger_mapped: Number,
) -> None:
    fixture_activated_instance.mocked_hidapi_device.set_left_stick_x_raw(left_stick_x_raw)
    fixture_activated_instance.mocked_hidapi_device.set_left_stick_y_raw(left_stick_y_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_stick_x_raw(right_stick_x_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_stick_y_raw(right_stick_y_raw)
    fixture_activated_instance.mocked_hidapi_device.set_left_trigger_raw(left_trigger_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_trigger_raw(right_trigger_raw)
    fixture_activated_instance.controller.wait_until_updated()
    assert left_stick_x_mapped == pytest.approx(fixture_activated_instance.controller.left_stick_x.value, rel=1e-4)
    assert left_stick_y_mapped == pytest.approx(fixture_activated_instance.controller.left_stick_y.value, rel=1e-4)
    assert right_stick_x_mapped == pytest.approx(fixture_activated_instance.controller.right_stick_x.value, rel=1e-4)
    assert right_stick_y_mapped == pytest.approx(fixture_activated_instance.controller.right_stick_y.value, rel=1e-4)
    assert left_trigger_mapped == pytest.approx(fixture_activated_instance.controller.left_trigger.value, rel=1e-4)
    assert right_trigger_mapped == pytest.approx(fixture_activated_instance.controller.right_trigger.value, rel=1e-4)


# @pytest.mark.skip(reason="temp disabled")
@pytest.mark.parametrize(
    'fixture_params_for_mocked_hidapi_device,fixture_params_for_controller_instance'
    ',left_stick_x_raw,left_stick_x_mapped'
    ',left_stick_y_raw,left_stick_y_mapped'
    ',right_stick_x_raw,right_stick_x_mapped'
    ',right_stick_y_raw,right_stick_y_mapped'
    ',left_trigger_raw,left_trigger_mapped'
    ',right_trigger_raw,right_trigger_mapped'
    , [
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW),
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW),
         127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW),
         128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW),
         255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         127, 127, 127, 128, 127, 127, 127, 128, 127, 127, 127, 127],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         128, 128, 128, 127, 128, 128, 128, 127, 128, 128, 128, 128],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.RAW_INVERTED),
         255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT),
         0, -128, 0, 127, 0, -128, 0, 127, 0, 0, 0, 0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT),
         127, -1, 127, 0, 127, -1, 127, 0, 127, 127, 127, 127],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT),
         128, 0, 128, -1, 128, 0, 128, -1, 128, 128, 128, 128],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT),
         255, 127, 255, -128, 255, 127, 255, -128, 255, 255, 255, 255],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         0, -128, 0, -128, 0, -128, 0, -128, 0, 0, 0, 0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         127, -1, 127, -1, 127, -1, 127, -1, 127, 127, 127, 127],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         128, 0, 128, 0, 128, 0, 128, 0, 128, 128, 128, 128],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.DEFAULT_INVERTED),
         255, 127, 255, 127, 255, 127, 255, 127, 255, 255, 255, 255],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED),
         0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, 0.0, 0, 0.0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED),
         127, 0.0, 127, 0.0, 127, 0.0, 127, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED),
         128, 0.0, 128, 0.0, 128, 0.0, 128, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED),
         255, 1.0, 255, -1.0, 255, 1.0, 255, -1.0, 255, 1.0, 255, 1.0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         0, -1.0, 0, -1.0, 0, -1.0, 0, -1.0, 0, 0.0, 0, 0.0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         127, 0.0, 127, 0.0, 127, 0.0, 127, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         128, 0.0, 128, 0.0, 128, 0.0, 128, 0.0, 127, 0.5, 127, 0.5],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.NORMALIZED_INVERTED),
         255, 1.00, 255, 1.00, 255, 1.00, 255, 1.00, 255, 1.0, 255, 1.0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.HUNDRED),
         0, -100, 0, 100, 0, -100, 0, 100, 0, 0, 0, 0],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.HUNDRED),
         127, 0, 127, 0, 127, 0, 127, 0, 127, 49, 127, 49],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.HUNDRED),
         128, 0, 128, 0, 128, 0, 128, 0, 128, 50, 128, 50],
        [ConnTypeMock.BT_01, ControllerInstanceParams(Mapping.HUNDRED),
         255, 100, 255, -100, 255, 100, 255, -100, 255, 100, 255, 100],
    ],
    indirect=['fixture_params_for_mocked_hidapi_device', 'fixture_params_for_controller_instance']
)
def test_mapping_bt01(
        fixture_params_for_mocked_hidapi_device: ConnTypeMock,
        fixture_params_for_controller_instance: ControllerInstanceParams,
        fixture_activated_instance: ControllerInstanceData,
        left_stick_x_raw: int,
        left_stick_x_mapped: Number,
        left_stick_y_raw: int,
        left_stick_y_mapped: Number,
        right_stick_x_raw: int,
        right_stick_x_mapped: Number,
        right_stick_y_raw: int,
        right_stick_y_mapped: Number,
        left_trigger_raw: int,
        left_trigger_mapped: Number,
        right_trigger_raw: int,
        right_trigger_mapped: Number,
) -> None:
    fixture_activated_instance.mocked_hidapi_device.set_left_stick_x_raw(left_stick_x_raw)
    fixture_activated_instance.mocked_hidapi_device.set_left_stick_y_raw(left_stick_y_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_stick_x_raw(right_stick_x_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_stick_y_raw(right_stick_y_raw)
    fixture_activated_instance.mocked_hidapi_device.set_left_trigger_raw(left_trigger_raw)
    fixture_activated_instance.mocked_hidapi_device.set_right_trigger_raw(right_trigger_raw)
    fixture_activated_instance.controller.wait_until_updated()
    assert left_stick_x_mapped == pytest.approx(fixture_activated_instance.controller.left_stick_x.value, rel=1e-4)
    assert left_stick_y_mapped == pytest.approx(fixture_activated_instance.controller.left_stick_y.value, rel=1e-4)
    assert right_stick_x_mapped == pytest.approx(fixture_activated_instance.controller.right_stick_x.value, rel=1e-4)
    assert right_stick_y_mapped == pytest.approx(fixture_activated_instance.controller.right_stick_y.value, rel=1e-4)
    assert left_trigger_mapped == pytest.approx(fixture_activated_instance.controller.left_trigger.value, rel=1e-4)
    assert right_trigger_mapped == pytest.approx(fixture_activated_instance.controller.right_trigger.value, rel=1e-4)
