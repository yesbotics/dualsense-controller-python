# DualSense™ controller for Python

Use the Sony DualSense™ controller (PlayStation 5 controller) with Python (3.10+)

## Contents

- [Requirements](#requirements)
- [Installation](#installation)
    - [Prerequisites for Windows](#prerequisites-for-windows)
    - [Prerequisites for Linux](#prerequisites-for-linux)
- [Usage](#usage)
- [Development](#development)
    - [Protocol](#protocol)
- [Sources](#sources)

## Requirements

- Linux
- Python 3.10+
- hidapi

## Installation

### Prerequisites for Linux

...

### Prerequisites for Windows

...

### Installation via PIP

```shell
pip install dualsense-controller
```

### Installation via Python Poetry

```shell
poetry add dualsense-controller
```

## Usage

Import the library and create an instance

```python
from dualsense_controller import DualSenseController

dualsense_controller = DualSenseController()
```

## Development

...

### Protocol

For communication between PC and controller there is a byte-based protocol, which has been deciphered to a large extent.
The meaning of individual bytes and byte sequences in both direction - from and to the controller - is documented in the
files [docs/dualsense-controller.ods](https://github.com/yesbotics/dualsense-controller-python/blob/main/docs/dualsense-controller.ods)
and [README_PROTOCOL.md](https://github.com/yesbotics/dualsense-controller-python/blob/main/README_PROTOCOL.md)

## Sources

This project's was heavily inspired by the following projects.
A lot of implementation details were borrowed and know-how were extracted from them.

- [DualSense explorer tool](https://github.com/nondebug/dualsense)
- [ds5ctl](https://github.com/theY4Kman/ds5ctl)
- [pydualsense](https://github.com/flok/pydualsense)
- [PS5 Library of USB_Host_Shield_2.0](https://github.com/felis/USB_Host_Shield_2.0#ps5-library)
- [DualSense on Windows \[API\]](https://github.com/Ohjurot/DualSense-Windows)

## Trademarks Notes

"PlayStation", "PlayStation Family Mark", "PS5 logo", "PS5", "DualSense" and "DUALSHOCK"
are registered trademarks or trademarks of Sony Interactive Entertainment Inc.
"SONY" is a registered trademark of Sony Corporation.
The authors are not affiliated in any kind with Sony Interactive Entertainment Inc.
