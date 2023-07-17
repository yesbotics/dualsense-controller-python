import threading
from threading import Thread
from time import sleep
from typing import Callable
from typing import Final

import hidapi
import pyee as pyee

from dualsense_controller import EventType, Event, AlreadyInitializedException, NotInitializedYetException
from dualsense_controller import NoDeviceDetectedException, InvalidDeviceIndexException

_VENDOR_ID: Final[int] = 0x054c
_PRODUCT_ID: Final[int] = 0x0ce6
_OUTPUT_REPORT_USB: Final[int] = 0x02
_OUTPUT_REPORT_BT: Final[int] = 0x31


class DualSenseController:

    @staticmethod
    def enumerate_devices() -> list[hidapi.DeviceInfo]:
        return [device_info for device_info in hidapi.enumerate(vendor_id=_VENDOR_ID)
                if device_info.vendor_id == _VENDOR_ID and device_info.product_id == _PRODUCT_ID]

    def __init__(self, device_index: int = 0):
        self._device_index: int = device_index
        self._hid_device: hidapi.Device | None = None
        self._event_emitter: pyee.EventEmitter = pyee.EventEmitter()
        self._run_thread: bool = False
        self._thread: Thread | None = None
        self._initialized: bool = False

    def add_event_listener(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        self._event_emitter.on(event_type.name, callback)

    def remove_event_listener(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        self._event_emitter.remove_listener(event_type.name, callback)

    def init(self) -> None:
        if self._initialized:
            raise AlreadyInitializedException
        self._initialized = True
        self._run_thread = True
        self._thread = threading.Thread(
            target=self._poll,
            daemon=True,
        )
        self._thread.start()

    def deinit(self) -> None:
        if not self._initialized:
            raise NotInitializedYetException
        self._run_thread = False
        self._thread.join()
        self._thread = None
        self._initialized = False

    def _poll(self) -> None:
        while self._run_thread:
            if self._hid_device is None:
                self._event_emitter.emit(
                    EventType.CONNECTION_LOOKUP.name,
                    Event(EventType.CONNECTION_LOOKUP, None)
                )
                try:
                    self._hid_device = self._open_device()
                    self._event_emitter.emit(
                        EventType.CONNECTION_STATE_CHANGE.name,
                        Event(EventType.CONNECTION_LOOKUP, True)
                    )
                except NoDeviceDetectedException:
                    print('NoHidDeviceDetectedException')
                    sleep(1)
            else:
                print('blubbblubb')
                sleep(1)
        self._hid_device.close()
        self._hid_device = None

    def _open_device(self) -> hidapi.Device:
        devices: list[hidapi.DeviceInfo] = DualSenseController.enumerate_devices()
        num_devices: int = len(devices)
        if num_devices < 1:
            raise NoDeviceDetectedException
        if num_devices < self._device_index + 1:
            raise InvalidDeviceIndexException(self._device_index)
        device_info: hidapi.DeviceInfo = devices[self._device_index]
        return hidapi.Device(vendor_id=device_info.vendor_id, product_id=device_info.product_id)
