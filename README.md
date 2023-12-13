# DualSense™ controller for Python

Use the Sony DualSense™ controller (PlayStation 5 controller) with Python.

![Teaser Image](teaser.jpg)

**Features:**

- Python support for Windows and Linux. See [Tested with](#tested-with) section.
- Connection via USB or Bluetooth
- Simple, flexible and intuitive event-based API
- Read and listen to all analog and digital inputs
- Read and listen to battery state
- Read and listen to touchpad
- Set lights (Microphone light and Player LEDs) and its brightness,
- Set the lightbar's color,
- Set haptic feedback
- Set adaptive triggers (experimental - work in progress)

**Limitations:**

- No support for older Python versions. Only Python 3.10+ supported
- Linux Kernel must be minimum 5.12+
- No macOS support (We are checking whether we can provide support at a later date)
- Requires third party Software (hidapi). See [Installation](#installation) section to get it working

## Contents

- [Tested with](#tested-with)
- [Requirements](#requirements)
- [Installation](#installation)
    - [Prerequisites for Windows](#prerequisites-for-windows)
    - [Prerequisites for Linux](#prerequisites-for-linux)
        - [HIDAPI](#hidapi)
        - [udev-rules](#udev-rules)
    - [Install the library](#install-the-library)
- [Usage](#usage)
    - [Getting started - Simple example](#getting-started---simple-example)
    - [List available devices](#list-available-devices)
    - [Initialization](#initialization)
    - [Lifecycle: Activation - Operation - Deactivation](#lifecycle-activation---operation---deactivation)
    - [Errors during operation](#errors-during-operation)
    - [Read and listen to Battery](#read-and-listen-to-battery)
    - [Listen to digital buttons](#listen-to-digital-buttons)
    - [Listen to analog buttons](#listen-to-analog-buttons)
    - [Listen to touch fingers](#listen-to-touch-fingers)
    - [Listen to Gyroscope, Accelerotmeter and Orientation](#listen-to-gyroscope-accelerotmeter-and-orientation)
    - [Set lightbar color](#set-lightbar-color)
    - [Set player LEDs](#set-player-leds)
    - [Set haptic feedback (Rumble)](#set-haptic-feedback-rumble)
    - [Set adaptive triggers](#set-adaptive-triggers)
    - [Behavioral Options](#behavioral-options)
        - [Value Mapping](#value-mapping)
    - [More Examples](#more-examples)
- [Development Notes](#development-notes)
    - [Protocol](#protocol)
- [Sources](#sources)
- [Contribution](#contribution)
- [Trademarks Notes](#trademarks-notes)
- [Photo Credits](#photo-credits)

## Tested with

Windows:

- Windows 10 Professional

Linux:

- Manjaro Linux (6.1.38-1-MANJARO (64-bit)), Python 3.11.x
- Ubuntu 22.04 Linux 64-bit, Python 3.10.x

## Requirements

- Linux
- Python 3.10+
- hidapi

## Installation

Some preparations have to be done before depending on your operating system:

### Prerequisites for Linux

#### HIDAPI on Linux

You need [HIDAPI library](https://github.com/libusb/hidapi) installed on your system.

For example on Ubuntu install it via:

```bash
sudo apt install libhidapi-dev
```

#### udev rules

For use the controller in Python without root privileges add the udev rule.

```bash
sudo cp res/70-dualsense.rules /etc/udev/rules.d
```

or create a file `/etd/udev/rules.d/70-dualsense.rules` with following content.

```
# USB
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0ce6", MODE="0666"
# Bluetooth
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", KERNELS=="0005:054C:0CE6.*", MODE="0666"
```

Then u have to activate the rule.

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Prerequisites for Windows

Just download the [latest release of HIDAPI](https://github.com/libusb/hidapi/releases).
Unzip the release zip file und then place the according `hidapi.dll` in your Workspace (i.e. `C:\Windows\System32`)
folder.
(from `x64` folder for 64-bit Windows or from `x86` folder for 32-bit Windows)

### Install the library

You can now go ahead and use the library within your projects.
Add either via [pip](https://pypi.org/project/pip/)

```shell
pip install --upgrade dualsense-controller
```

or when you prefer [Python Poetry](https://python-poetry.org/) as Packaging and Dependency Management solution,
then add via

```shell
poetry add dualsense-controller
```

## Usage

### Getting started - Simple example

Following example enables rumble on cross button press and disables rumble on release.
Example program stops on PS button pressed.

```python
from time import sleep

from dualsense_controller import DualSenseController

# list availabe devices and throw exception when tzhere is no device detected
device_infos = DualSenseController.enumerate_devices()
if len(device_infos) < 1:
    raise Exception('No DualSense Controller available.')

# flag, which keeps program alive
is_running = True

# create an instance, use fiŕst available device
controller = DualSenseController()


# switches the keep alive flag, which stops the below loop
def stop():
    global is_running
    is_running = False


# callback, when cross button is pressed, which enables rumble
def on_cross_btn_pressed():
    print('cross button pressed')
    controller.left_rumble.set(255)
    controller.right_rumble.set(255)


# callback, when cross button is released, which disables rumble
def on_cross_btn_released():
    print('cross button released')
    controller.left_rumble.set(0)
    controller.right_rumble.set(0)


# callback, when PlayStation button is pressed
# stop program
def on_ps_btn_pressed():
    print('PS button released -> stop')
    stop()


# callback, when unintended error occurs,
# i.e. physically disconnecting the controller during operation
# stop program
def on_error(error):
    print(f'Opps! an error occured: {error}')
    stop()


# register the button callbacks
controller.btn_cross.on_down(on_cross_btn_pressed)
controller.btn_cross.on_up(on_cross_btn_released)
controller.btn_ps.on_down(on_ps_btn_pressed)

# register the error callback
controller.on_error(on_error)

# enable/connect the device
controller.activate()

# start keep alive loop, controller inputs and callbacks are handled in a second thread
while is_running:
    sleep(0.001)

# disable/disconnect controller device
controller.deactivate()
```

### List available devices

Check whether devices are connected and detected

```python
device_infos = DualSenseController.enumerate_devices()
if len(device_infos) < 1:
    raise Exception('No DualSense Controller available.')
```

### Initialization

You can initialize Controller by passing an index, (`amount of devices - 1`)

```python
controller = DualSenseController(device_index_or_device_info=0)
```

an DeviceInfo object, obtained from devices list

```python
controller = DualSenseController(device_index_or_device_info=device_infos[0])
```

or just pass nothing, which tries to use first device

```python
controller = DualSenseController()
```

### Lifecycle: Activation - Operation - Deactivation

The controller is intended to be used in such a way that you activate it first.
Since the controller communication now takes place in a separate thread,
you must ensure that your program remains alive,
e.g. by using a while loop (possibly with a termination condition).
At the end you have to deactivate the controller.

```python
is_running = True

controller.activate()

while is_running:
    sleep(0.001)

controller.deactivate()
```

Alternatively, you can also use the controller with context manager,
which activates and deactivates controller automatically

```python
is_running = True

with active_dualsense_controller() as controller:
    while is_running:
        sleep(0.001)
```

### Errors during operation

In order to be able to react to unforeseen errors during operation,
such as a physical disconnect, you can handle such events in a callback.

```python
def on_error(error):
    print(f'an unforseen error occured {error}')
    # handle error
    # ...
```

register the callback via

```python
controller.on_error(on_error)
```

### Read and listen to Battery

You can read out the charge level and charge status of the battery as follows

```python
batt = controller.battery.value
print(batt)
```

or listen to changes (especially while conneted via Bluetooth):

```python
def on_battery_change(battery) -> None:
    print(f'on battery change: {battery}')


def on_battery_lower_than(battery_level) -> None:
    print(f'on battery low: {battery_level}')


def on_battery_charging(battery_level) -> None:
    print(f'on battery charging: {battery_level}')


def on_battery_discharging(battery_level) -> None:
    print(f'on battery discharging: {battery_level}')


controller.battery.on_change(on_battery_change)
controller.battery.on_lower_than(20, on_battery_lower_than)
controller.battery.on_charging(on_battery_charging)
controller.battery.on_discharging(on_battery_discharging)
```

### Listen to digital buttons

Digital Buttons are `Up`, `Down`, `Left`, `Right`, `Cross`, `Square`, `Circle`, `Triangle`,
`L1`, `L2`, `L3`,`R1`, `R2`, `R3`, `Touchpad click`, `PlayStation`, `Mute`, `Create` and `Options`
You can listen to them in several ways:
Detect if button is pressed, released or its has value changed

```python
def on_cross_btn_pressed():
    print('cross button pressed')


def on_cross_btn_released():
    print('cross button_released')


def on_cross_btn_changed(pressed):
    print(f'cross button is pressed: {pressed}')


controller.btn_cross.on_down(on_cross_btn_pressed)
controller.btn_cross.on_up(on_cross_btn_released)
controller.btn_cross.on_change(on_cross_btn_changed)
```

### Listen to analog buttons

Analog Buttons are the sticks and the trigger keys
Attention: trigger keys can be used analog and digital. `L2` and `L3` are digital buttons too

```python
def on_left_trigger(value):
    print(f'left trigger changed: {value}')


def on_left_stick_x_changed(left_stick_x):
    print(f'on_left_stick_x_changed: {left_stick_x}')


def on_left_stick_y_changed(left_stick_y):
    print(f'on_left_stick_y_changed: {left_stick_y}')


def on_left_stick_changed(left_stick):
    print(f'on_left_stick_changed: {left_stick}')


controller.left_trigger.on_change(on_left_trigger)
controller.left_stick_x.on_change(on_left_stick_x_changed)
controller.left_stick_y.on_change(on_left_stick_y_changed)
controller.left_stick.on_change(on_left_stick_changed)

```

### Listen to touch fingers

```python
def on_touch_finger_1(value):
    print(f'touch finger 1 changed: {value}')


def on_touch_finger_2(value):
    print(f'touch finger 2 changed: {value}')


controller.touch_finger_1.on_change(on_touch_finger_1)
controller.touch_finger_2.on_change(on_touch_finger_2)
```

### Listen to Gyroscope, Accelerotmeter and Orientation

```python
def on_gyroscope_change(gyroscope):
    print(f'on_gyroscope_change: {gyroscope}')


def on_accelerometer_change(accelerometer):
    print(f'on_accelerometer_change: {accelerometer}')


def on_orientation_change(orientation):
    print(f'on_orientation_change: {orientation}')


controller.gyroscope.on_change(on_gyroscope_change)
controller.accelerometer.on_change(on_accelerometer_change)
controller.orientation.on_change(on_orientation_change)
```

### Set lightbar color

Set the color via predefined values

```python
controller.lightbar.set_color_red()
# controller.lightbar.set_color_green()
# controller.lightbar.set_color_blue()
# controller.lightbar.set_color_white()
# controller.lightbar.set_color_black()
```

or with custom RGB values

```python
controller.lightbar.set_color(88, 10, 200)
```

### Set player LEDs

Turn on all LEDs or specific ones

```python
controller.player_leds.set_all()
# controller.player_leds.set_inner()
# controller.player_leds.set_outer()
# controller.player_leds.set_center_and_outer()
# controller.player_leds.set_center()
```

or turn off all

```python
controller.player_leds.set_off()
```

and modify their brightness

```python
controller.player_leds.set_brightness_high()
# controller.player_leds.set_brightness_medium()
# controller.player_leds.set_brightness_low()
```

### Set haptic Feedback (Rumble)

The haptic feedback is controlled by the left and right builtin rumble motors.

**Attention:** the according rumble values depend on the chosen [Value Mapping](#value-mapping).
By default, it is a value between 0 and 255.

```python
controller.left_rumble.set(0)  # no rumble
# controller.left_rumble.set(128)  # medium rumble
# controller.left_rumble.set(255) # strong rumble
```

### Set adaptive Triggers

You can use different trigger effects. By default, the triggers have **no resistance**,
which corresponds to the following

```python
controller.left_trigger.effect.set_no_resistance()
```

**Continuous resistance** effect is defined a start position and a strength

```python
controller.left_trigger.effect.set_continuous_resistance(start_pos=0, force=255)  # full resistance
# controller.left_trigger.effect.set_continuous_resistance(start_pos=127, force=255) # full resist. starts at middle pos
# controller.left_trigger.effect.set_continuous_resistance(start_pos=0, force=128)  # medium resistance
```

**Section resistance** effect means only a section has resitance

```python
controller.left_trigger.effect.set_section_resistance(start_pos=70, end_pos=100, force=255)  # full
# controller.left_trigger.effect.set_section_resistance(start_pos=70,end_pos=100,force=10) # low resistance
```

**Work in Progress**: The **Extended Effect** is the most complicated effect.
To be honest, we don't really know how it works and which parameters are necessary to achieve according result.
Unfortunately there is no official documentation from Sony
and the other libraries that served as a source of inspiration don't really help to enlighten us either.
For this reason, feel free to experiment with it.
We are working on a solution to be able to offer at least a few presets,
which should then be included in future releases of this library.
We would be pleased to receive your cooperation and suggestions on how we should handle it.

```python
controller.left_trigger.effect.set_effect_extended()
```

The most powerful trigger effect is **Custom effect**.
We offer this interface to provide the greatest possible freedom by making it possible to send
raw values (8-bit unsigned integer: 0 - 255) to the controller.
Here, too, you are welcome to play with different values.
And we welcome any insights that help us to offer useful presets.

```python
controller.left_trigger.effect.set_custom_effect(param1, param2, param3, param4, param5, param6, param7)
```

### Behavioral Options

The behaviour of some aspects can be adjusted via the following optional parameters during initialization.

#### Value Mapping

You can change the value mapping for analog values, like stick axis, trigger values and rumble intensity
By default the stick axis values are mapped from -128 to 127 (default mapping)
and the trigger values from 0 to 255, which means the stick axis default position values are 0
and trigers default position values are 0.
Optional stick deadzones should be adjusted properly depeneding on the mapping, i.e. value 3 is fine
when the stick axis values range from -128 to 127. But it is too high,
when stick range is interpreted as -1.0 to 1.0 (normalized mapping),
then u should use a deadzone which is smaller than 1.

To apply a custom mapping, i.e. normalized mapping (-1.0 to 1.0) pass it while initialization:

```python
controller = DualSenseController(
    # ...
    mapping=Mapping.NORMALIZED,
    # ...
)
```

Available mappings are:

- `Mapping.RAW`: stick x axis values from 0 to 255, stick y axis values from 0 to 255, trigger values from 0 to 255,
  rumble from 0 to 255
- `Mapping.RAW_INVERTED`: same as `Mapping.RAW` but stick y axis values inverted.
- `Mapping.DEFAULT`: stick x axis values from -128 to 127, stick y axis values from 127 to -128, trigger values from 0
  to 255, rumble from 0 to 255
- `Mapping.DEFAULT_INVERTED`: same as `Mapping.DEFAULT` but stick y axis values inverted.
- `Mapping.NORMALIZED`: stick x axis values from -1.0 to 1.0, stick y axis values from 1.0 to -1.0, trigger values from
  0.0 to 1.0, rumble from 0 to 1.0
- `Mapping.NORMALIZED_INVERTED`: same as `Mapping.NORMALIZED` but stick y axis values inverted.
- `Mapping.HUNDRED`:

### More Examples

Not all funcionality is explicitly explained here, so take a look at the example files here,
to see more use cases take a look into the `./src/examples`:

## Development Notes

...

### USB Sniffing on Windows with Wireshark/TShark and USBPcap

Wireshark with USBPcap install is required. Ensure that your Wireshark and USBPcapCMD binaries are in the
Windows Path variable.

1. find controller in USB tree to detect Root Device, i.e. `\\.\USBPcap3`
    ```cmd
    USBPcapCMD.exe
    ```
2. Run Capture in Wireshark for that device, start an app which permanently sends Data to controller
   like [nondebug Dualsense Explorer](https://nondebug.github.io/dualsense/dualsense-explorer.html) (Chrome browser
   required)
3. In Wireshark find Destination Number for appropriate device (out) i.e. `3.8.3`
4. Run script:
    ```cmd
    python tools_dev/shark/shark.py USBPcap3 3.8.3
    ```

The output should look like:

```
02 ff f7 00 00 00 00 00 00 00 10 26 90 a0 ff 00 00 00 00 00 00 00 26 90 a0 ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 02 00 00 ff ff ff
operating_mode: 02
flags_physics: ff
flags_controls: f7
motor_right: 00
motor_left: 00
microphone_led: 00
microphone_mute: 10
right_trigger: 26 90 a0 ff 00 00 00 00
left_trigger: 26 90 a0 ff 00 00 00 00
led_options: 00
lightbar_pulse_options: 02
player_leds_brightness: 00
player_leds_enable: 00
color: ff ff ff

```

### Protocol

For communication between PC and controller there is a byte-based protocol, which has been deciphered to a large extent.
The meaning of individual bytes and byte sequences in both direction - from and to the controller - is documented in the
files [docs/dualsense-controller.ods](https://github.com/yesbotics/dualsense-controller-python/blob/main/docs/dualsense-controller.ods)
and [README_PROTOCOL.md](https://github.com/yesbotics/dualsense-controller-python/blob/main/README_PROTOCOL.md)

## Sources

This project's was heavily inspired by the following projects.
A lot of implementation details were borrowed and know-how were extracted from them.

- [pydualsense](https://github.com/flok/pydualsense)
- [DualSense explorer tool](https://github.com/nondebug/dualsense)
- [ds5ctl](https://github.com/theY4Kman/ds5ctl)
- [PS5 Library of USB_Host_Shield_2.0](https://github.com/felis/USB_Host_Shield_2.0#ps5-library)
- [DualSense on Windows \[API\]](https://github.com/Ohjurot/DualSense-Windows)
- [Factories for all DualSense trigger effects](https://gist.github.com/Nielk1/6d54cc2c00d2201ccb8c2720ad7538db?permalink_comment_id=4250586)
- [Game Controller Collective Wiki: Sony DualSense](https://controllers.fandom.com/wiki/Sony_DualSense#Input_Reports)

Libs

- [hidapi-usb](https://github.com/flok/hidapi-cffi)
- [pyhidapi](https://github.com/apmorton/pyhidapi)
- [cython-hidapi](https://github.com/trezor/cython-hidapi)
- [hidapi](https://github.com/libusb/hidapi)
- [hidapitester](https://github.com/todbot/hidapitester)

## Contribution

We welcome any input from others to help us improve this software.
Feel free to send us suggestions.
In particular, collaboration on the documentation,
the haptic feedback (Rumble) and the adaptive triggers APIs are especially welcome.

## Trademarks Notes

"PlayStation", "PlayStation Family Mark", "PS5 logo", "PS5", "DualSense" and "DUALSHOCK"
are registered trademarks or trademarks of Sony Interactive Entertainment Inc.
"SONY" is a registered trademark of Sony Corporation.
The authors are not affiliated in any kind with Sony Interactive Entertainment Inc.

## Photo Credits

Teaser Image: Original photo
by <a href="https://unsplash.com/@martzzl?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Marcel
Strauß</a>
on <a href="https://unsplash.com/photos/gray-and-black-xbox-one-game-controller-WO4DxFdA3dY?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">
Unsplash</a>