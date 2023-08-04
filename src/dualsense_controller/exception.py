from abc import ABC


class AbstractBaseException(ABC, Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class NoDeviceDetectedException(AbstractBaseException):
    def __init__(self):
        super().__init__('No DualSense device detected')


class InvalidDeviceIndexException(AbstractBaseException):
    def __init__(self, idx: int):
        super().__init__(f'Invalid DualSense device index given {idx}')


class InvalidInReportLengthException(AbstractBaseException):
    def __init__(self):
        super().__init__(f'Invalid connection type')
