# DualSense™ controller for Python

Use the Sony DualSense™ controller (PlayStation 5 controller) with Python (3.10+) in Windows or Linux (Kernel 5.12+)

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
- [Development](#development)
    - [Protocol](#protocol)
- [Sources](#sources)
- [Trademarks Notes](#trademarks-notes)

## Tested with

Windows:

- Windows 10 Pro

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

### Basic Usage

#### Import

```python
from dualsense_controller import DualSenseController, Mapping
```

#### List available devices

Check whether devices are connected and detected

```python
device_infos = DualSenseController.enumerate_devices()
if len(device_infos) < 1:
    raise Exception('No DualSense Controller available.')
```

#### Initialization

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

### Listen for digital buttons

You can listen to digital button changes in severals ways: 
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



### Options

#### Value Mapping

You can change the value mapping for analog values, like stick axis, trigger values and rumble intensity
Per default the stick axis values are mapped from -128 to 127 (default mapping)
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

### Examples

Please take a look at the example files here, to dive see more complex use cases:

```
/src/examples/example.py
/src/examples/example_trigger.py
/src/examples/contextmanager_usage_example.py
```

## Development

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

Libs

- [hidapi-usb](https://github.com/flok/hidapi-cffi)
- [pyhidapi](https://github.com/apmorton/pyhidapi)
- [cython-hidapi](https://github.com/trezor/cython-hidapi)
- [hidapi](https://github.com/libusb/hidapi)
- [hidapitester](https://github.com/todbot/hidapitester)

## Trademarks Notes

"PlayStation", "PlayStation Family Mark", "PS5 logo", "PS5", "DualSense" and "DUALSHOCK"
are registered trademarks or trademarks of Sony Interactive Entertainment Inc.
"SONY" is a registered trademark of Sony Corporation.
The authors are not affiliated in any kind with Sony Interactive Entertainment Inc.
