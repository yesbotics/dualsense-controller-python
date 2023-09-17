#!/bin/bash

tshark -i USBPcap3 -Y "usb.dst == 3.8.3" --hexdump frames --hexdump delimit --hexdump noascii | ./watch.sh