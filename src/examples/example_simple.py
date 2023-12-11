from dualsense_controller import DualSenseController, Mapping


def on_button_pressed():
    pass


device_infos = DualSenseController.enumerate_devices()
if len(device_infos) < 1:
    raise Exception('No DualSense Controller available.')

controller = DualSenseController(mapping=Mapping.NORMALIZED)
controller.activate()


def on_cross_btn_pressed():
    print('cross button pressed')


def on_cross_btn_released():
    print('cross button_released')


def on_cross_btn_changed(pressed):
    print(f'cross button is pressed: {pressed}')


controller.btn_cross.on_down(on_cross_btn_pressed)
controller.btn_cross.on_up(on_cross_btn_released)
controller.btn_cross.on_change(on_cross_btn_changed)
