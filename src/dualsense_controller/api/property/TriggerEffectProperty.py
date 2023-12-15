from typing import List, Tuple

from deprecated import deprecated

from dualsense_controller.api.property.base import Property
from dualsense_controller.core.state.write_state.enum import TriggerEffectMode
from dualsense_controller.core.state.write_state.value_type import TriggerEffect


class TriggerEffectProperty(Property[TriggerEffect]):

    @deprecated(version='0.2.0', reason='Method is deprecated. Use no_resistance() method instead.')
    def set_no_resistance(self) -> None:
        self.no_resistance()

    @deprecated(version='0.2.0', reason='Method is deprecated. Use continuous_resistance() method instead.')
    def set_continuous_resistance(self, start_pos: int = 0, force: int = 255) -> None:
        self.continuous_resistance(start_pos, force)

    @deprecated(version='0.2.0', reason='Method is deprecated. Use section_resistance() method instead.')
    def set_section_resistance(self, start_pos: int = 70, end_pos: int = 100, force: int = 255) -> None:
        self.section_resistance(start_pos, end_pos, force)

    @deprecated(version='0.2.0', reason='Method is deprecated. Use effect_extended() method instead.')
    def set_effect_extended(
            self,
            start_pos: int = 0,
            keep_effect: bool = False,
            begin_force: int = 0,
            middle_force: int = 0,
            end_force: int = 0,
            frequency: int = 0,
    ) -> None:
        self.effect_extended(start_pos, keep_effect, begin_force, middle_force, end_force, frequency)

    @deprecated(version='0.2.0', reason='Method is deprecated. Use custom_effect() method instead.')
    def set_custom_effect(
            self,
            mode: int | TriggerEffectMode = TriggerEffectMode.NO_RESISTANCE,
            param1: int = 0x00,
            param2: int = 0x00,
            param3: int = 0x00,
            param4: int = 0x00,
            param5: int = 0x00,
            param6: int = 0x00,
            param7: int = 0x00,
    ) -> None:
        self.custom_effect(mode, param1, param2, param3, param4, param5, param6, param7)

    def no_resistance(self) -> None:
        self._set(TriggerEffectMode.NO_RESISTANCE)

    def continuous_resistance(self, start_pos: int = 0, force: int = 255) -> None:
        self._set(TriggerEffectMode.CONTINUOUS_RESISTANCE, start_pos, force)

    def section_resistance(self, start_pos: int = 70, end_pos: int = 100, force: int = 255) -> None:
        self._set(TriggerEffectMode.SECTION_RESISTANCE, start_pos, end_pos, force)

    def effect_extended(
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

    def custom_effect(
            self,
            mode: int | TriggerEffectMode = TriggerEffectMode.NO_RESISTANCE,
            param1: int = 0x00,
            param2: int = 0x00,
            param3: int = 0x00,
            param4: int = 0x00,
            param5: int = 0x00,
            param6: int = 0x00,
            param7: int = 0x00,
    ) -> None:
        self._set(
            mode=mode,
            param1=param1,
            param2=param2,
            param3=param3,
            param4=param4,
            param5=param5,
            param6=param6,
            param7=0x00,
            param8=0x00,
            param9=param7,
            param10=0x00,
        )

    # new

    def off(self) -> None:
        self._set(TriggerEffectMode.OFF)

    def feedback(self, start_pos: int = 0, strength: int = 8) -> None:
        """
        Trigger will resist movement beyond the start position.
        The trigger status nybble will report 0 before the effect and 1 when in the effect.
        This is an offical effect and is expected to be present in future DualSense firmware.
        :param start_pos: The starting zone of the trigger effect. Must be between 0 and 9 inclusive.
        :param strength: The force of the resistance. Must be between 0 and 8 inclusive.
        """

        assert start_pos >= 0, 'start_pos must be minimum 0'
        assert start_pos <= 9, 'start_pos must be maximum 9'
        assert strength >= 0, 'strength must be minimum 0'
        assert strength <= 8, 'strength must be maximum 8'

        force: int = (strength - 1) & 0x07
        force_zones: int = 0
        active_zones: int = 0
        for i in range(start_pos, 10):
            force_zones |= (force << (3 * i))
            active_zones |= (1 << i)

        self._set(
            mode=TriggerEffectMode.FEEDBACK,
            param1=((active_zones >> 0) & 0xff),
            param2=((active_zones >> 8) & 0xff),
            param3=((force_zones >> 0) & 0xff),
            param4=((force_zones >> 8) & 0xff),
            param5=((force_zones >> 16) & 0xff),
            param6=((force_zones >> 24) & 0xff),
            # (byte)((forceZones >> 32) & 0xff); // need 64bit for this, but we already have enough space
            param7=0x00,
            # (byte)((forceZones >> 40) & 0xff); // need 64bit for this, but we already have enough space
            param8=0x00,
            param9=0x00,
            param10=0x00
        )

    def weapon(self, start_pos: int = 2, end_pos: int = 5, strength: int = 8) -> None:
        """
        Trigger will resist movement beyond the start position until the end position.
        The trigger status nybble will report 0 before the effect and 1 when in the effect,
        and 2 after until again before the start position.
        This is an offical effect and is expected to be present in future DualSense firmware.
        :param start_pos: The starting zone of the trigger effect. Must be between 2 and 7 inclusive.
        :param end_pos: The ending zone of the trigger effect. Must be between start_pos + 1 and 8 inclusive.
        :param strength: The force of the resistance. Must be between 0 and 8 inclusive.
        """
        assert start_pos >= 2, 'start_pos must be minimum 2'
        assert start_pos <= 7, 'start_pos must be maximum 7'
        assert end_pos >= start_pos + 1, f'end_pos must be minimum start_pos ({start_pos}) + 1'
        assert start_pos <= 8, 'end_pos must be maximum 8'
        assert strength >= 0, 'strength must be minimum 0'
        assert strength <= 8, 'strength must be maximum 8'

        start_and_stop_zones = ((1 << start_pos) | (1 << end_pos))

        self._set(
            mode=TriggerEffectMode.WEAPON,
            param1=((start_and_stop_zones >> 0) & 0xff),
            param2=((start_and_stop_zones >> 8) & 0xff),
            # this is actually packed into 3 bits, but since it's only one why bother with the fancy code?
            param3=(strength - 1),
            param4=0x00,
            param5=0x00,
            param6=0x00,
            param7=0x00,
            param8=0x00,
            param9=0x00,
            param10=0x00
        )

    def multiple_position_feedback(
            self,
            strengths: list[int] | tuple[int, ...] = (8, 8, 0, 0, 0, 0, 8, 8, 0, 0)
    ) -> None:
        """
        Trigger will resist movement at varrying strengths in 10 regions.
        This is an offical effect and is expected to be present in future DualSense firmware.
        This is an offical effect and is expected to be present in future DualSense firmware.
        :param strengths: Array of 10 resistance values for zones 0 through 9. Must be between 0 and 8 inclusive.
        """
        assert isinstance(strengths, (List, Tuple)), 'strengths must be tuple or list'
        assert len([s for s in strengths if 0 <= s <= 8]) == 10, 'strength values must be between 0 and 8'

        force_zones: int = 0
        active_zones: int = 0
        for i in range(0, 10):
            if strengths[i] > 0:
                force: int = ((strengths[i] - 1) & 0x07)
                force_zones |= (force << (3 * i))
                active_zones |= (1 << i)

        self._set(
            mode=TriggerEffectMode.FEEDBACK,
            param1=((active_zones >> 0) & 0xff),
            param2=((active_zones >> 8) & 0xff),
            param3=((force_zones >> 0) & 0xff),
            param4=((force_zones >> 8) & 0xff),
            param5=((force_zones >> 16) & 0xff),
            param6=((force_zones >> 24) & 0xff),
            # (byte)((forceZones >> 32) & 0xff); // need 64bit for this, but we already have enough space
            param7=0x00,
            # (byte)((forceZones >> 40) & 0xff); // need 64bit for this, but we already have enough space
            param8=0x00,
            param9=0x00,
            param10=0x00
        )

    def _set(
            self,
            mode: int | TriggerEffectMode,
            param1: int = 0x00,
            param2: int = 0x00,
            param3: int = 0x00,
            param4: int = 0x00,
            param5: int = 0x00,
            param6: int = 0x00,
            param7: int = 0x00,
            param8: int = 0x00,
            param9: int = 0x00,
            param10: int = 0x00,
    ) -> None:
        self._set_value(TriggerEffect(
            mode=mode,
            param1=param1,
            param2=param2,
            param3=param3,
            param4=param4,
            param5=param5,
            param6=param6,
            param7=param7,
            param8=param8,
            param9=param9,
            param10=param10,
        ))
