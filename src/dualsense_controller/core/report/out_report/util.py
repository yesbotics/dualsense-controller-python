def clamp(value: int, val_min: int, val_max: int) -> int:
    return min(val_max, max(val_min, value))


def clamp_byte(value: int) -> int:
    return min(255, max(0, value))
