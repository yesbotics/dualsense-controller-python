class StateValueCalc:

    @classmethod
    def sensor_axis(cls, v1: int, v0: int) -> int:
        sub: int = ((v1 << 8) | v0)
        return sub if sub > 0x7FFF else sub - 0x10000

    @classmethod
    def touch_active(cls, t_0: int) -> bool:
        return bool(t_0 & 0x80)

    @classmethod
    def touch_id(cls, t_0: int) -> int:
        return t_0 & 0x7F

    @classmethod
    def touch_x(cls, t_2: int, t_1: int) -> int:
        return ((t_2 & 0x0F) << 8) | t_1

    @classmethod
    def touch_y(cls, t_3: int, t_2: int) -> int:
        return (t_3 << 4) | ((t_2 & 0xF0) >> 4)

    @classmethod
    def batt_level_percentage(cls, b: int) -> float:
        batt_level_raw: int = b & 0x0f
        if batt_level_raw > 8:
            batt_level_raw = 8
        batt_level: float = batt_level_raw / 8
        return batt_level * 100
