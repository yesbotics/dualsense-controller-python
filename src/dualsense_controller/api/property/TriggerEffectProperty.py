from typing import List, Tuple

from deprecated import deprecated

from dualsense_controller.api.property.base import Property
from dualsense_controller.core.state.write_state.enum import TriggerEffectMode
from dualsense_controller.core.state.write_state.value_type import TriggerEffect


class TriggerEffectProperty(Property[TriggerEffect]):

    # ############################## CUSTOM/BASE ################################

    def set(
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

    # ############################## DEPRECATED ################################

    @deprecated(
        version='0.2.0',
        reason='Method is deprecated and will may be removed in future. Use no_resistance() method instead.'
    )
    def set_no_resistance(self) -> None:
        self.no_resistance()

    @deprecated(
        version='0.2.0',
        reason='Method is deprecated and will may be removed in future. Use continuous_resistance() method instead.'
    )
    def set_continuous_resistance(self, start_position: int = 0, force: int = 255) -> None:
        self.continuous_resistance(start_position, force)

    @deprecated(
        version='0.2.0',
        reason='Method is deprecated and will may be removed in future. Use section_resistance() method instead.'
    )
    def set_section_resistance(self, start_position: int = 70, end_position: int = 100, force: int = 255) -> None:
        self.section_resistance(start_position, end_position, force)

    @deprecated(
        version='0.2.0',
        reason='Method is deprecated and will may be removed in future. Use effect_extended() method instead.'
    )
    def set_effect_extended(
            self,
            start_position: int = 0,
            keep_effect: bool = False,
            begin_force: int = 0,
            middle_force: int = 0,
            end_force: int = 0,
            frequency: int = 0,
    ) -> None:
        self.effect_extended(start_position, keep_effect, begin_force, middle_force, end_force, frequency)

    @deprecated(version='0.2.0', reason='Method is deprecated and will may be removed in future.')
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
        self.set(
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

    # ############################## SIMPLE (OLD) ################################

    def no_resistance(self) -> None:
        self.set(TriggerEffectMode.NO_RESISTANCE)

    def continuous_resistance(self, start_position: int = 0, force: int = 255) -> None:
        """
        Simplistic Feedback effect data generator.
        This is not an offical effect and has an offical alternative. It may be removed in a future DualSense firmware.
        :param start_position: The starting zone of the trigger effect.
        :param force: The force of the resistance.
        """
        self.set(TriggerEffectMode.CONTINUOUS_RESISTANCE, start_position, force)

    def section_resistance(self, start_position: int = 70, end_position: int = 100, force: int = 255) -> None:
        """
        Simplistic Weapon effect data generator.
        This is not an offical effect and has an offical alternative. It may be removed in a future DualSense firmware.
        :param start_position: The starting zone of the trigger effect.
        :param end_position: The ending zone of the trigger effect.
        :param force: The force of the resistance.
        """
        self.set(TriggerEffectMode.SECTION_RESISTANCE, start_position, end_position, force)

    # TODO: not working properly
    def effect_extended(
            self,
            start_position: int = 0,
            keep_effect: bool = True,
            begin_force: int = 0,
            middle_force: int = 0,
            end_force: int = 0,
            frequency: int = 0,
    ) -> None:
        self.set(
            mode=TriggerEffectMode.EFFECT_EXTENDED,
            param1=0xff - start_position,
            param2=0x02 if keep_effect else 0x00,
            param4=begin_force,
            param5=middle_force,
            param6=end_force,
            param9=frequency if frequency >= 1 else 1,
        )

    def simple_vibration(self, start_position: int = 0, amplitude: int = 255, frequency: int = 8) -> None:
        """
        Simplistic Vibration effect data generator.
        This is not an offical effect and has an offical alternative. It may be removed in a future DualSense firmware.
        :param start_position: The starting zone of the trigger effect.
        :param amplitude: Strength of the automatic cycling action.
        :param frequency: Frequency of the automatic cycling action in hertz.
        """
        if frequency <= 0 or amplitude <= 0:
            return
        self.set(
            mode=TriggerEffectMode.SIMPLE_VIBRATION,
            param1=frequency,
            param2=amplitude,
            param3=start_position,
            param4=0x00,
            param5=0x00,
            param6=0x00,
            param7=0x00,
            param8=0x00,
            param9=0x00,
            param10=0x00,
        )

    # ############################## OFFICIAL ################################

    def off(self) -> None:
        self.set(TriggerEffectMode.OFF)

    def feedback(self, start_position: int = 0, strength: int = 8) -> None:
        """
        Trigger will resist movement beyond the start position.
        The trigger status nybble will report 0 before the effect and 1 when in the effect.
        This is an offical effect and is expected to be present in future DualSense firmware.
        :param start_position: The starting zone of the trigger effect. Must be between 0 and 9 inclusive.
        :param strength: The force of the resistance. Must be between 0 and 8 inclusive.
        """

        assert start_position >= 0, 'start_position must be minimum 0'
        assert start_position <= 9, 'start_position must be maximum 9'
        assert strength >= 0, 'strength must be minimum 0'
        assert strength <= 8, 'strength must be maximum 8'

        force: int = (strength - 1) & 0x07
        force_zones: int = 0
        active_zones: int = 0
        for i in range(start_position, 10):
            force_zones |= (force << (3 * i))
            active_zones |= (1 << i)

        self.set(
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

    def weapon(self, start_position: int = 2, end_position: int = 5, strength: int = 8) -> None:
        """
        Trigger will resist movement beyond the start position until the end position.
        The trigger status nybble will report 0 before the effect and 1 when in the effect,
        and 2 after until again before the start position.
        This is an offical effect and is expected to be present in future DualSense firmware.
        :param start_position: The starting zone of the trigger effect. Must be between 2 and 7 inclusive.
        :param end_position: The ending zone of the trigger effect. Must be between start_position + 1 and 8 inclusive.
        :param strength: The force of the resistance. Must be between 0 and 8 inclusive.
        """
        assert start_position >= 2, 'start_position must be minimum 2'
        assert start_position <= 7, 'start_position must be maximum 7'
        assert end_position >= start_position + 1, f'end_position must be minimum start_position ({start_position}) + 1'
        assert start_position <= 8, 'end_position must be maximum 8'
        assert strength >= 0, 'strength must be minimum 0'
        assert strength <= 8, 'strength must be maximum 8'

        start_and_stop_zones = ((1 << start_position) | (1 << end_position))

        self.set(
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

        self.set(
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

    # TODO: not working properly
    def vibration(self, start_position: int = 0, amplitude: int = 2, frequency: int = 3) -> None:
        """
        Trigger will vibrate with the input amplitude and frequency beyond the start position.
        The trigger status nybble will report 0 before the effect and 1 when in the effect.
        This is an offical effect and is expected to be present in future DualSense firmware.
        :param start_position: The starting zone of the trigger effect. Must be between 0 and 9 inclusive.
        :param amplitude: Strength of the automatic cycling action. Must be between 0 and 8 inclusive.
        :param frequency: Frequency of the automatic cycling action in hertz.
        """

        assert 0 <= start_position <= 9, 'start_position must be between 0 and 9 inclusive'
        assert 0 <= amplitude <= 8, 'start_position must be between 0 and 8 inclusive'
        assert 0 <= frequency, 'frequency must be between 0 and 8 inclusive'

        if amplitude == 0 or frequency == 0:
            return

        strength_value: int = (amplitude - 1) & 0x07
        amplitude_zones: int = 0
        active_zones: int = 0
        for i in range(start_position, 10):
            amplitude_zones |= strength_value << (3 * i)
            active_zones |= (1 << i)

        self.set(
            mode=TriggerEffectMode.VIBRATION,
            param1=((active_zones >> 0) & 0xff),
            param2=((active_zones >> 8) & 0xff),
            param3=((amplitude_zones >> 0) & 0xff),
            param4=((amplitude_zones >> 8) & 0xff),
            param5=((amplitude_zones >> 16) & 0xff),
            param6=((amplitude_zones >> 24) & 0xff),
            # (byte)((amplitude_zones >> 32) & 0xff); // need 64bit for this, but we already have enough space
            param7=0x00,
            # (byte)((amplitude_zones >> 40) & 0xff); // need 64bit for this, but we already have enough space
            param8=0x00,
            param9=frequency,
            param10=0x00
        )

    # TODO: not working properly
    def multiple_position_vibration(
            self,
            frequency: int = 8,
            amplitudes: list[int] | tuple[int, ...] = (4, 4, 4, 0, 0, 0, 0, 4, 4, 4)
    ) -> None:
        """
        Trigger will vibrate movement at varrying amplitudes and one frequency in 10 regions.
        This is an offical effect and is expected to be present in future DualSense firmware.
        Note this factory's results may not perform as expected.
        :param amplitudes: Array of 10 strength values for zones 0 through 9. Must be between 0 and 8 inclusive.</param>
        :param frequency: Frequency of the automatic cycling action in hertz.</param>
        """

        assert isinstance(amplitudes, (List, Tuple)), 'amplitudes must be tuple or list'
        assert len([s for s in amplitudes if 0 <= s <= 8]) == 10, 'amplitude values must be between 0 and 8'

        strength_zones: int = 0
        active_zones: int = 0
        for i in range(0, 10):
            if amplitudes[i] > 0:
                strength: int = ((amplitudes[i] - 1) & 0x07)
                strength_zones |= (strength << (3 * i))
                active_zones |= (1 << i)

        self.set(
            mode=TriggerEffectMode.VIBRATION,
            param1=((active_zones >> 0) & 0xff),
            param2=((active_zones >> 8) & 0xff),
            param3=((strength_zones >> 0) & 0xff),
            param4=((strength_zones >> 8) & 0xff),
            param5=((strength_zones >> 16) & 0xff),
            param6=((strength_zones >> 24) & 0xff),
            param7=0x00,  # (byte)((forceZones >> 32) & 0xff); // need 64bit for this, but we already have enough space
            param8=0x00,  # (byte)((forceZones >> 40) & 0xff); // need 64bit for this, but we already have enough space
            param9=frequency,
            param10=0x00,
        )

    def slope_feedback(self, start_position: int = 0, end_position: int = 9, start_strength: int = 1,
                       end_strength: int = 4) -> None:
        """
        Trigger will resist movement at a linear range of strengths.
        This is an offical effect and is expected to be present in future DualSense firmware.
        :param start_position: The starting zone of the trigger effect. Must be between 0 and 8 inclusive.
        :param end_position: The ending zone of the trigger effect. Must be between start_position + 1 and 9 inclusive.
        :param start_strength: The force of the resistance at the start. Must be between 1 and 8 inclusive.
        :param end_strength: The force of the resistance at the end. Must be between 1 and 8 inclusive.
        """
        assert 0 <= start_position <= 8, 'start_position must be between 0 and 8 inclusive.'
        assert start_position < end_position <= 9, 'end_position must be between start_position + 1 and 9 inclusive.'
        assert 1 <= start_strength <= 8, 'start_strength must be between 1 and 8 inclusive.'
        assert 1 <= end_strength <= 8, 'end_strength must be between 1 and 8 inclusive.'
        strengths: list[int] = [0] * 10
        slope: float = 1.0 * (end_strength - start_strength) / (end_position - start_position)

        for i in range(start_position, 10):
            strengths[i] = round(start_strength + (slope * (i - start_position))) if i <= end_position else end_strength

        self.multiple_position_feedback(strengths)

    # ############################## UNOFFICIAL ################################

    def bow(self, start_position: int = 1, end_position: int = 4, strength: int = 1, snap_force: int = 8):
        """
        The effect resembles the Weapon
        effect, however there is a snap-back force that attempts to reset the trigger.
        This is not an offical effect and may be removed in a future DualSense firmware.
        :param start_position: The starting zone of the trigger effect. Must be between 0 and 8 inclusive.
        :param end_position: The ending zone of the trigger effect. Must be between start_position +1 and 8 inclusive.
        :param strength: The force of the resistance. Must be between 0 and 8 inclusive.
        :param snap_force: The force of the snap-back. Must be between 0 and 8 inclusive.
        """
        assert 0 <= start_position <= 8, 'start_position must be between 0 and 8 inclusive.'
        assert start_position < end_position <= 9, 'end_position must be between start_position + 1 and 9 inclusive.'
        assert 0 <= strength <= 9, 'strength must be between 0 and 8 inclusive.'
        assert 0 <= snap_force <= 9, 'snapForce must be between 0 and 8 inclusive.'

        if end_position == 0 or strength == 0 or snap_force == 0:
            return
        start_and_stop_zones = ((1 << start_position) | (1 << end_position))
        force_pair = ((((strength - 1) & 0x07) << (3 * 0)) | (((snap_force - 1) & 0x07) << (3 * 1)))

        self.set(
            mode=TriggerEffectMode.BOW,
            param1=((start_and_stop_zones >> 0) & 0xff),
            param2=((start_and_stop_zones >> 8) & 0xff),
            param3=((force_pair >> 0) & 0xff),
            param4=((force_pair >> 8) & 0xff),
            param5=0x00,
            param6=0x00,
            param7=0x00,
            param8=0x00,
            param9=0x00,
            param10=0x00,
        )

    def galloping(
            self,
            start_position: int = 0,
            end_position: int = 9,
            first_foot: int = 4,
            second_foot: int = 7,
            frequency: int = 2
    ) -> None:
        """
        Trigger will oscillate in a rythmic pattern resembling galloping. Note that the
        effect is only discernable at low frequency values.
        This is not an offical effect and may be removed in a future DualSense firmware.
        :param start_position:The starting zone of the trigger effect. Must be between 0 and 8 inclusive.
        :param end_position:The ending zone of the trigger effect. Must be between start_position + 1 and 9 inclusive.
        :param first_foot:Position of second foot in cycle. Must be between 0 and 6 inclusive.
        :param second_foot:Position of second foot in cycle. Must be between first_foot + 1 and 7 inclusive.
        :param frequency:Frequency of the automatic cycling action in hertz.
        """

        assert 0 <= start_position <= 8, 'start_position must be between 0 and 8 inclusive.'
        assert start_position < end_position <= 9, 'start_position must be between start_position + 1 and 9 inclusive.'
        assert 0 <= first_foot <= 6, 'first_foot must be between 0 and 6 inclusive.'
        assert first_foot < second_foot <= 7, 'second_foot must be between first_foot + 1 and 7 inclusive.'
        assert 0 <= frequency, 'second_foot must be greater equal 0'

        if frequency == 0:
            return

        start_and_stop_zones: int = ((1 << start_position) | (1 << end_position))
        time_and_ratio: int = (((second_foot & 0x07) << (3 * 0)) | ((first_foot & 0x07) << (3 * 1)))

        self.set(
            mode=TriggerEffectMode.GALLOPING,
            param1=((start_and_stop_zones >> 0) & 0xff),
            param2=((start_and_stop_zones >> 8) & 0xff),
            param3=((time_and_ratio >> 0) & 0xff),
            # this is actually packed into 3 bits, but since it's only one why bother with the fancy code?
            param4=frequency,
            param5=0x00,
            param6=0x00,
            param7=0x00,
            param8=0x00,
            param9=0x00,
            param10=0x00,
        )

    def machine(
            self,
            start_position: int = 1,
            end_position: int = 9,
            amplitude_a: int = 2,
            amplitude_b: int = 7,
            frequency: int = 5,
            period: int = 3
    ) -> None:
        """
        This effect resembles Vibration
        but will oscilate between two amplitudes.
        This is not an offical effect and may be removed in a future DualSense firmware.
        :param start_position: The starting zone of the trigger effect. Must be between 0 and 8 inclusive
        :param end_position: The ending zone of the trigger effect. Must be between start_position + 1 and 9 inclusive
        :param amplitude_a: Primary strength of cycling action. Must be between 0 and 7 inclusive
        :param amplitude_b: Secondary strength of cycling action. Must be between 0 and 7 inclusive
        :param frequency: Frequency of the automatic cycling action in hertz
        :param period: Period of the oscillation between amplitudeA amplitudeB in tenths of a second
        """

        assert 0 <= start_position <= 8, 'start_position must be between 0 and 8 inclusive'
        assert 0 <= end_position <= 9, 'end_position must be between start_position + 1 and 9 inclusive'
        assert 0 <= amplitude_a <= 7, 'amplitude_a must be between 0 and 7 inclusive'
        assert 0 <= amplitude_b <= 7, 'amplitude_b must be between 0 and 7 inclusive'

        if frequency == 0:
            return
        start_and_stop_zones: int = ((1 << start_position) | (1 << end_position))
        strength_pair: int = (((amplitude_a & 0x07) << (3 * 0)) | ((amplitude_b & 0x07) << (3 * 1)))

        self.set(
            mode=TriggerEffectMode.MACHINE,
            param1=((start_and_stop_zones >> 0) & 0xff),
            param2=((start_and_stop_zones >> 8) & 0xff),
            param3=((strength_pair >> 0) & 0xff),
            param4=frequency,
            param5=period,
            param6=0x00,
            param7=0x00,
            param8=0x00,
            param9=0x00,
            param10=0x00
        )

    # ############################## ReWASD ################################

    def full_press(self) -> None:
        self.section_resistance(start_position=0x90, end_position=0xa0, force=0xff)

    def soft_press(self) -> None:
        self.section_resistance(start_position=0x70, end_position=0xa0, force=0xff)

    def medium_press(self) -> None:
        self.section_resistance(start_position=0x45, end_position=0xa0, force=0xff)

    def hard_press(self) -> None:
        self.section_resistance(start_position=0x20, end_position=0xa0, force=0xff)

    def pulse(self) -> None:
        self.section_resistance(start_position=0x00, end_position=0x00, force=0x00)

    def choppy(self) -> None:
        self.set(
            mode=TriggerEffectMode.FEEDBACK,
            param1=0x02,  # region enables
            param2=0x27,  # region enables
            param3=0x18,  # reWASD uses 0x1f here, but some bits apply to regions not enabled above
            param4=0x00,
            param5=0x00,  # reWASD uses 0x27 here, but some bits apply to regions not enabled above
            param6=0x26,
            param7=0x00,
            param8=0x00,
            param9=0x00,
            param10=0x00,
        )

    def soft_rigidity(self) -> None:
        self.continuous_resistance(start_position=0x00, force=0x00)

    def medium_rigidity(self) -> None:
        self.continuous_resistance(start_position=0x00, force=0x64)

    def max_rigidity(self) -> None:
        self.continuous_resistance(start_position=0x00, force=0xdc)

    def half_press(self) -> None:
        self.continuous_resistance(start_position=0x55, force=0x64)

    # TODO: not working properly
    def rifle(self, frequency: int = 10) -> None:
        """
        Rifle vibration effect data generator with some wasted bits.
        Bad coding from reWASD was faithfully replicated.
        :param frequency: Frequency of the automatic cycling action in hertz. Must be between 2 and 20 inclusive.</param>
        """
        assert 2 <= frequency <= 20, 'frequency must be between 2 and 20 inclusive'

        self.set(
            mode=TriggerEffectMode.VIBRATION,
            param1=0x00,
            param2=0x03,  # reWASD uses 0xFF here but the top 6 bits are unused
            param3=0x00,
            param4=0x00,
            param5=0x00,
            param6=0x3F,  # reWASD uses 0xFF here but the top 2 bits are unused
            param7=0x00,
            param8=0x00,
            param9=frequency,
            param10=0x00,
        )

    # TODO: not working properly
    def vibration_2(self, strength: int = 220, frequency: int = 30) -> None:
        """
        Vibration effect with incorrect strength handling.
        Bad coding from reWASD was faithfully replicated.
        :param strength: Strength of the automatic cycling action. Must be between 1 and 255 inclusive.
        This is two 3 bit numbers with the remaining 2 high bits unused. Yes, reWASD uses this value incorrectly.
        :param frequency: Frequency of the automatic cycling action in hertz. Must be between 1 and 255 inclusive.
        """
        if strength < 1:
            return
        if frequency < 1:
            return

        self.set(
            mode=TriggerEffectMode.VIBRATION,
            param1=0x00,  # reWASD uses 0x1E here but this is invalid and is ignored save for minor glitches
            param2=0x03,  # reWASD uses 0xFF here but the top 6 bits are unused
            param3=0x00,
            param4=0x00,
            param5=0x00,
            param6=strength,  # reWASD maxes at 0xFF here but the top 2 bits are unused
            param7=0x00,
            param8=0x00,
            param9=frequency,
            param10=0x00,
        )
