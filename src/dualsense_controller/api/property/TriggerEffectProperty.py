from dualsense_controller.api.property.base import Property
from dualsense_controller.core.state.write_state.enum import TriggerEffectMode
from dualsense_controller.core.state.write_state.value_type import TriggerEffect


class TriggerEffectProperty(Property[TriggerEffect]):

    def set_no_resistance(self) -> None:
        self._set(
            mode=TriggerEffectMode.NO_RESISTANCE,
        )

    def set_continuous_resistance(
            self,
            start_pos: int = 0,
            force: int = 255
    ) -> None:
        self._set(
            mode=TriggerEffectMode.CONTINUOUS_RESISTANCE,
            param1=start_pos,
            param2=force,
        )

    def set_section_resistance(
            self,
            start_pos: int = 70,
            end_pos: int = 100,
            force: int = 255,
    ) -> None:
        self._set(
            mode=TriggerEffectMode.SECTION_RESISTANCE,
            param1=start_pos,
            param2=end_pos,
            param3=force,
        )


    # TODO: wip
    def set_preset_automatic_gun(self, start: int = 0, strength: int = 8, frequency: int = 9) -> None:
        assert 0 <= start <= 9, "start value must be minimum 0 and maximum 9"
        assert 0 <= strength <= 8, "start strength must be minimum 0 and maximum 8"
        assert 0 <= frequency <= 13, "start frequency must be minimum 0 and maximum 13"
        start_byte_1: int = 256 - (1 << start) if start < 9 else 0
        start_byte_2: int = 3 if start < 9 else 2
        print(start_byte_1)
        self._set(
            mode=TriggerEffectMode.EFFECT_EXTENDED,
            param1=255,
            param2=255,
            param3=255,
            param4=255,
            param5=255,
            param6=255,
            param7=13
        )

    def set_effect_extended(
            self,
            start_pos: int = 0,
            keep_effect: bool = False,
            begin_force: int = 0,
            middle_force: int = 0,
            end_force: int = 0,
            frequency: int = 0,
    ) -> None:
        self._set(
            mode=TriggerEffectMode.EFFECT_EXTENDED,
            param1=0xff - start_pos,
            param2=0x02 if keep_effect else 0x00,
            param3=begin_force,
            param4=middle_force,
            param5=end_force,
            param6=frequency,
        )

    # @TODO: Check if needed. Does not work currently
    # def set_calibrate(self) -> None:
    #     self._set(
    #         mode=TriggerEffectMode.CALIBRATE,
    #     )

    # @TODO Function is WIP!
    # def set_bow(
    #         self,
    #         start_pos: int = 0,
    #         end_pos: int = 0,
    #         force: int = 0,
    #         snap_force: int = 0,
    # ) -> None:
    #     self._set(
    #         mode=TriggerEffectMode.BOW,
    #         param1=start_pos,
    #         param2=end_pos,
    #         param3=force,
    #         param4=snap_force,
    #     )

    def set_custom_effect(
            self,
            mode: int | TriggerEffectMode = TriggerEffectMode.NO_RESISTANCE,
            param1: int = 0,
            param2: int = 0,
            param3: int = 0,
            param4: int = 0,
            param5: int = 0,
            param6: int = 0,
            param7: int = 0,
    ) -> None:
        self._set(
            mode=mode,
            param1=param1,
            param2=param2,
            param3=param3,
            param4=param4,
            param5=param5,
            param6=param6,
            param7=param7,
        )

    def _set(
            self,
            mode: int | TriggerEffectMode = None,
            param1: int = None,
            param2: int = None,
            param3: int = None,
            param4: int = None,
            param5: int = None,
            param6: int = None,
            param7: int = None,
    ) -> None:
        before: TriggerEffect = self._get_value()
        # TODO: Check if previous value is dangerous
        self._set_value(TriggerEffect(
            mode=mode if mode is not None else before.mode,
            param1=param1 if param1 is not None else before.param1,
            param2=param2 if param2 is not None else before.param2,
            param3=param3 if param3 is not None else before.param3,
            param4=param4 if param4 is not None else before.param4,
            param5=param5 if param5 is not None else before.param5,
            param6=param6 if param6 is not None else before.param6,
            param7=param7 if param7 is not None else before.param7,
        ))
