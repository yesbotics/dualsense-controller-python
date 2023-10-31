from typing import Final

from dualsense_controller.core.Benchmarker import Benchmark, Benchmarker
from dualsense_controller.core.HidControllerDevice import HidControllerDevice
from dualsense_controller.core.enum import ConnectionType, EventType
from dualsense_controller.core.hidapi.hidapi import DeviceInfo
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.state.State import State
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.mapping.enum import StateValueMapping
from dualsense_controller.core.state.read_state.ReadStates import ReadStates
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.read_state.value_type import Connection
from dualsense_controller.core.state.typedef import Number, StateChangeCallback
from dualsense_controller.core.state.write_state.WriteStates import WriteStates
from dualsense_controller.core.state.write_state.enum import WriteStateName
from dualsense_controller.core.typedef import EmptyCallback
from dualsense_controller.core.util import format_exception


class DualSenseControllerCore:

    # ######################################### STATIC  ##########################################v
    @staticmethod
    def enumerate_devices() -> list[DeviceInfo]:
        return HidControllerDevice.enumerate_devices()

    # ######################################### BASE  ##########################################v
    @property
    def is_initialized(self) -> bool:
        return self._hid_controller_device.is_opened

    @property
    def read_states(self) -> ReadStates:
        return self._read_states

    @property
    def write_states(self) -> WriteStates:
        return self._write_states

    @property
    def connection_type(self) -> ConnectionType:
        return self._hid_controller_device.connection_type

    # ######################################### SPECIAL STATES  ##########################################v

    @property
    def connection_state(self) -> State[Connection]:
        return self._connection_state

    @property
    def update_benchmark_state(self) -> State[Benchmark]:
        return self._update_benchmark_state

    @property
    def exception_state(self) -> State[Exception]:
        return self._exception_state

    # ######################################### MAIN  ##########################################v
    def __init__(
            self,
            # ##### BASE  #####
            device_index_or_device_info: int | DeviceInfo = 0,
            # ##### FEELING  #####
            left_joystick_deadzone: Number = 0,
            right_joystick_deadzone: Number = 0,
            left_trigger_deadzone: Number = 0,
            right_trigger_deadzone: Number = 0,
            gyroscope_threshold: int = 0,
            accelerometer_threshold: int = 0,
            orientation_threshold: int = 0,
            state_value_mapping: StateValueMapping = StateValueMapping.DEFAULT,
            # ##### CORE #####
            enforce_update: bool = False,
            can_update_itself: bool = True,
    ):

        # HARDWARE
        self._hid_controller_device: HidControllerDevice = HidControllerDevice(device_index_or_device_info)

        # SPECIAL STATES
        self._connection_state: Final[State[Connection]] = State(
            name=EventType.CONNECTION_CHANGE, ignore_none=False
        )

        self._update_benchmark_state: Final[State[Benchmark]] = State(
            name=EventType.UPDATE_BENCHMARK, ignore_none=True
        )

        self._exception_state: Final[State[Exception]] = State(
            name=EventType.EXCEPTION, ignore_none=False
        )

        # MAIN
        self._update_benchmark: Final[Benchmarker] = Benchmarker()

        state_value_mapper: StateValueMapper = StateValueMapper(
            mapping=state_value_mapping,
            left_joystick_deadzone=left_joystick_deadzone,
            right_joystick_deadzone=right_joystick_deadzone,
            left_trigger_deadzone=left_trigger_deadzone,
            right_trigger_deadzone=right_trigger_deadzone,
            gyroscope_threshold=gyroscope_threshold,
            accelerometer_threshold=accelerometer_threshold,
            orientation_threshold=orientation_threshold,
        )

        self._read_states: Final[ReadStates] = ReadStates(
            state_value_mapper=state_value_mapper,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        self._write_states: Final[WriteStates] = WriteStates(
            state_value_mapper=state_value_mapper,
        )

        self._hid_controller_device.on_exception(self._on_thread_exception)
        self._hid_controller_device.on_in_report(self._on_in_report)

    def on_updated(self, callback: EmptyCallback) -> None:
        self._read_states.on_updated(callback)

    def once_updated(self, callback: EmptyCallback) -> None:
        self._read_states.once_updated(callback)

    def wait_until_updated(self) -> None:

        wait: bool = True

        def on_updated() -> None:
            nonlocal wait
            wait = False

        self._read_states.once_updated(on_updated)
        while wait:
            pass

    def on_connection_change(self, callback: StateChangeCallback):
        self._connection_state.on_change(callback)

    def once_connection_change(self, callback: StateChangeCallback):
        self._connection_state.once_change(callback)

    def on_state_change(self, state_name: ReadStateName | StateChangeCallback, callback: StateChangeCallback = None):
        self._read_states.on_change(state_name, callback)

    def once_state_change(self, state_name: ReadStateName | StateChangeCallback, callback: StateChangeCallback = None):
        self._read_states.once_change(state_name, callback)

    def on_any_state_change(self, callback: StateChangeCallback):
        self._read_states.on_any_change(callback)

    def once_any_state_change(self, callback: StateChangeCallback):
        self._read_states.once_any_change(callback)

    def set_state(self, state_name: WriteStateName, value: Number):
        self._write_states.set_value(state_name, value)

    def init(self) -> None:
        assert not self._hid_controller_device.is_opened, 'already opened'
        self._hid_controller_device.open()
        self._connection_state.value = Connection(True, self._hid_controller_device.connection_type)

    def deinit(self) -> None:
        assert self._hid_controller_device.is_opened, 'not opened yet'
        self._hid_controller_device.close()
        self._connection_state.value = Connection(False, self._hid_controller_device.connection_type)

    def _on_in_report(self, in_report: InReport) -> None:

        self._read_states.update(in_report, self._hid_controller_device.connection_type)

        if self._write_states.has_changed:
            # print(f'Sending report.')
            self._write_states.update_out_report(self._hid_controller_device.out_report)
            self._write_states.set_unchanged()
            self._hid_controller_device.write()

        if self._update_benchmark_state.has_listeners:
            self._update_benchmark_state.value = self._update_benchmark.update()

    def _on_thread_exception(self, exception: Exception) -> None:
        self._exception_state.value = exception
        print('An Exception in the loop thread occured:', format_exception(exception))
