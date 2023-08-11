from enum import Enum

from dualsense_controller.core.state.mapping.common import Float, FromTo, StateValueMappingData


class StateValueMapping(Enum):
    # # no need to fill StateValueMapping.RAW, only for illustration
    # # stick y-axis: 0 ... 255, trigger: 0 ... 255
    # RAW = StateValueMappingData(
    #     left_stick_x=FromTo(0, 255, 0, 255),
    #     left_stick_y=FromTo(0, 255, 0, 255),
    #     left_stick_deadzone=FromTo(0, 255, 0, 255),
    #     right_stick_x=FromTo(0, 255, 0, 255),
    #     right_stick_y=FromTo(0, 255, 0, 255),
    #     right_stick_deadzone=FromTo(0, 255, 0, 255),
    #     left_trigger=FromTo(0, 255, 0, 255),
    #     left_trigger_deadzone=FromTo(0, 255, 0, 255),
    #     right_trigger=FromTo(0, 255, 0, 255),
    #     right_trigger_deadzone=FromTo(0, 255, 0, 255),
    #     set_motor_left=FromTo(0, 255, 0, 255),
    #     set_motor_right=FromTo(0, 255, 0, 255),
    # ),
    # # thats why
    RAW = None

    # stick y-axis: -100 ... 100, trigger: 0 ... 100
    HUNDRED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -100, 100),
        left_stick_y=FromTo(0, 255, 100, -100),
        left_stick_deadzone=FromTo(0, 255, 0, 100),
        right_stick_x=FromTo(0, 255, -100, 100),
        right_stick_y=FromTo(0, 255, 100, -100),
        right_stick_deadzone=FromTo(0, 255, 0, 100),
        left_trigger=FromTo(0, 255, 0, 100),
        left_trigger_deadzone=FromTo(0, 255, 0, 100),
        right_trigger=FromTo(0, 255, 0, 100),
        right_trigger_deadzone=FromTo(0, 255, 0, 100),
        set_motor_left=FromTo(0, 255, 0, 100),
        set_motor_right=FromTo(0, 255, 0, 100),
    )

    # stick y-axis: 255 ... 0, trigger: 0 ... 255
    RAW_INVERTED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, 0, 255),
        left_stick_y=FromTo(0, 255, 255, 0),
        right_stick_x=FromTo(0, 255, 0, 255),
        right_stick_y=FromTo(0, 255, 255, 0),
        # undefined maps handled like StateValueMapping.RAW
    )

    DEFAULT = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -128, 127),
        left_stick_y=FromTo(0, 255, 127, -128),
        right_stick_x=FromTo(0, 255, -128, 127),
        right_stick_y=FromTo(0, 255, 127, -128),
        # undefined maps handled like StateValueMapping.RAW
    )

    DEFAULT_INVERTED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -128, 127),
        left_stick_y=FromTo(0, 255, -128, 127),
        right_stick_x=FromTo(0, 255, -128, 127),
        right_stick_y=FromTo(0, 255, -128, 127),
        # undefined maps handled like StateValueMapping.RAW
    )

    NORMALIZED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        left_stick_y=FromTo(0, 255, 1.0, -1.0, to_type=Float()),
        left_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        right_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        right_stick_y=FromTo(0, 255, 1.0, -1.0, to_type=Float()),
        right_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        left_trigger=FromTo(0, 255, 0, 1.0, to_type=Float()),
        left_trigger_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_trigger=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_trigger_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_left=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_right=FromTo(0, 255, 0, 1.0, to_type=Float()),
    )

    NORMALIZED_INVERTED = StateValueMappingData(
        left_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        left_stick_y=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        left_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        right_stick_x=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        right_stick_y=FromTo(0, 255, -1.0, 1.0, to_type=Float()),
        right_stick_deadzone=FromTo(0, 127, 0, 1.0, to_type=Float()),
        left_trigger=FromTo(0, 255, 0, 1.0, to_type=Float()),
        left_trigger_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_trigger=FromTo(0, 255, 0, 1.0, to_type=Float()),
        right_trigger_deadzone=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_left=FromTo(0, 255, 0, 1.0, to_type=Float()),
        set_motor_right=FromTo(0, 255, 0, 1.0, to_type=Float()),
    )
