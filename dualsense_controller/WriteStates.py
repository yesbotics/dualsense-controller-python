from typing import Type, Generic

from dualsense_controller import State
from dualsense_controller.common import ReadStateName, StateChangeCallback, AnyStateChangeCallback, ConnectionType, \
    WriteStateName, ValueType
from dualsense_controller.reports import InReport, OutReport, Usb01OutReport, Bt01OutReport, Bt31OutReport
from dualsense_controller.exceptions import InvalidConnectionTypeException


class WriteStates:

    def __init__(
            self,
    ):
        super().__init__()

        self._changed = False
        self._states_dict: dict[WriteStateName, State] = {}

        self._create_state(WriteStateName.LIGHTBAR_RED, int, 0xff)
        self._create_state(WriteStateName.LIGHTBAR_GREEN, int, 0xff)
        self._create_state(WriteStateName.LIGHTBAR_BLUE, int, 0xff)
        self._create_state(WriteStateName.MOTOR_LEFT, int, 0x00)
        self._create_state(WriteStateName.MOTOR_RIGHT, int, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_MODE, int, 0x26)
        self._create_state(WriteStateName.L2_EFFECT_PARAM1, int, 0x90)
        self._create_state(WriteStateName.L2_EFFECT_PARAM2, int, 0xA0)
        self._create_state(WriteStateName.L2_EFFECT_PARAM3, int, 0xFF)
        self._create_state(WriteStateName.L2_EFFECT_PARAM4, int, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_PARAM5, int, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_PARAM6, int, 0x00)
        self._create_state(WriteStateName.L2_EFFECT_PARAM7, int, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_MODE, int, 0x26)
        self._create_state(WriteStateName.R2_EFFECT_PARAM1, int, 0x90)
        self._create_state(WriteStateName.R2_EFFECT_PARAM2, int, 0xA0)
        self._create_state(WriteStateName.R2_EFFECT_PARAM3, int, 0xFF)
        self._create_state(WriteStateName.R2_EFFECT_PARAM4, int, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_PARAM5, int, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_PARAM6, int, 0x00)
        self._create_state(WriteStateName.R2_EFFECT_PARAM7, int, 0x00)

    # @property
    # def states_dict(self) -> dict[ReadStateName, State]:
    #     return self._states_dict

    @property
    def changed(self) -> bool:
        return self._changed

    def set_unchanged(self):
        self._changed = False

    def set_value(self, name: WriteStateName, value):
        self._get_state(name).value = value

    def update_out_report(self, out_report: OutReport):
        out_report.lightbar_red = self._get_state(WriteStateName.LIGHTBAR_RED).value
        out_report.lightbar_green = self._get_state(WriteStateName.LIGHTBAR_GREEN).value
        out_report.lightbar_blue = self._get_state(WriteStateName.LIGHTBAR_BLUE).value
        out_report.motor_left = self._get_state(WriteStateName.MOTOR_LEFT).value
        out_report.motor_right = self._get_state(WriteStateName.MOTOR_RIGHT).value
        out_report.l2_effect_mode = self._get_state(WriteStateName.L2_EFFECT_MODE).value
        out_report.l2_effect_param1 = self._get_state(WriteStateName.L2_EFFECT_PARAM1).value
        out_report.l2_effect_param2 = self._get_state(WriteStateName.L2_EFFECT_PARAM2).value
        out_report.l2_effect_param3 = self._get_state(WriteStateName.L2_EFFECT_PARAM3).value
        out_report.l2_effect_param4 = self._get_state(WriteStateName.L2_EFFECT_PARAM4).value
        out_report.l2_effect_param5 = self._get_state(WriteStateName.L2_EFFECT_PARAM5).value
        out_report.l2_effect_param6 = self._get_state(WriteStateName.L2_EFFECT_PARAM6).value
        out_report.l2_effect_param7 = self._get_state(WriteStateName.L2_EFFECT_PARAM7).value
        out_report.r2_effect_mode = self._get_state(WriteStateName.R2_EFFECT_MODE).value
        out_report.r2_effect_param1 = self._get_state(WriteStateName.R2_EFFECT_PARAM1).value
        out_report.r2_effect_param2 = self._get_state(WriteStateName.R2_EFFECT_PARAM2).value
        out_report.r2_effect_param3 = self._get_state(WriteStateName.R2_EFFECT_PARAM3).value
        out_report.r2_effect_param4 = self._get_state(WriteStateName.R2_EFFECT_PARAM4).value
        out_report.r2_effect_param5 = self._get_state(WriteStateName.R2_EFFECT_PARAM5).value
        out_report.r2_effect_param6 = self._get_state(WriteStateName.R2_EFFECT_PARAM6).value
        out_report.r2_effect_param7 = self._get_state(WriteStateName.R2_EFFECT_PARAM7).value

    def _on_change(self, state_name: WriteStateName, _: bool, value: int):
        # print(F'State written: {state_name}')
        self._changed = True

    def _create_state(self, name: WriteStateName, data_type: Type, start_value) -> None:
        self._states_dict[name] = State[data_type](name, start_value)
        self._states_dict[name].on_change(self._on_change)

    def _get_state(self, name: WriteStateName) -> State:
        return self._states_dict[name]
