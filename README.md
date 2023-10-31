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

- Windows 10 Pro (TODO)

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

The detailed usage documentation is work in progress. Please take a look to the example files here: 

```
/src/examples/example.py
/src/examples/example_trigger.py
/src/examples/contextmanager_usage_example.py
```

[//]: # (Import the library and create an instance)

[//]: # ()
[//]: # (```python)

[//]: # (from dualsense_controller import DualSenseController)

[//]: # ()
[//]: # (dualsense_controller = DualSenseController&#40;&#41;)

[//]: # (```)

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
   like [nondebug Dualsense Explorer](https://nondebug.github.io/dualsense/dualsense-explorer.html) (Chrome browser required)
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
