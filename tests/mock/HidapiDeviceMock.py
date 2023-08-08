from tests.mock.common import ConnTypeMock


class _BaseDeviceMock:

    def __init__(self, conn_type: ConnTypeMock = ConnTypeMock.USB_01):
        if conn_type == ConnTypeMock.BT_01:
            raise NotImplementedError
        self._conn_type: ConnTypeMock = conn_type

    def write(self, data: bytes):
        pass

    def read(self, _: int, **kwargs) -> bytes:
        return self._conn_type.value

    def close(self):
        pass


class MockedHidapiDevice(_BaseDeviceMock):

    def set_left_stick_y_byte(self, value: int):

        match self._conn_type:
            case ConnTypeMock.USB_01:
                self._conn_type.value[2] = value
            case ConnTypeMock.BT_31:
                self._conn_type.value[3] = value
            case ConnTypeMock.BT_01:
                self._conn_type.value[2] = value
