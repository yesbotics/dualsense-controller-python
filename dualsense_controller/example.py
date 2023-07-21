from time import sleep

from dualsense_controller import DualSenseController, EventType, ConnectionLookupEvent, ConnectionChangeEvent, \
    StateChangeEvent, StateName


class Example:
    def __init__(self):

        dsc_connect_once: DualSenseController = DualSenseController(
            device_index=0,
            enable_connection_lookup=False,
            analog_threshold=2,
            gyro_threshold=30,
            accelerometer_threshold=50,
        )
        dsc_connect_once.add_event_listener(EventType.STATE_CHANGE, self._on_state_change)
        dsc_connect_once.init()
        while True:
            sleep(1)

        # # Usage methond 1 (enable_connection_lookup=False):
        # # Try to connect, if fails nothing nmore happens
        # print('Try to connect...')
        # dsc_connect_once: DualSenseController = DualSenseController(
        #     device_index=0,
        #     enable_connection_lookup=False
        # )
        # dsc_connect_once.add_event_listener(EventType.CONNECTION_CHANGE, self._on_connection_state_change)
        # dsc_connect_once.add_event_listener(EventType.STATE_CHANGE, self._on_state_change)
        # try:
        #     dsc_connect_once.init()
        #     print('...Successfully connected')
        #     sleep(5)
        #     print('Disconnect now...')
        #     dsc_connect_once.deinit()
        #     print('...successfully disconnected')
        # except Exception as e:
        #     print(f'...result: {e}')
        #     print('...unsuccessfull')
        #
        # print()
        # print()
        #
        # # Usage methond 2 (enable_connection_lookup=True):
        # # Instance and internal thread is active and trrigger event on connect/disconnect
        # print('Periodically look for connection...')
        # dsc_keep_connecting: DualSenseController = DualSenseController(
        #     device_index=0,
        #     enable_connection_lookup=True,
        #     connection_lookup_interval=0.5
        # )
        # dsc_keep_connecting.add_event_listener(EventType.CONNECTION_LOOKUP, self._on_connection_lookup)
        # dsc_keep_connecting.add_event_listener(EventType.CONNECTION_CHANGE, self._on_connection_state_change)
        # dsc_keep_connecting.add_event_listener(EventType.STATE_CHANGE, self._on_state_change)
        # dsc_keep_connecting.init()
        # sleep(5)
        # print('Stop looking for connection...')
        # dsc_keep_connecting.deinit()
        # print('...done')

    def _on_connection_lookup(self, evt: ConnectionLookupEvent) -> None:
        print(f'...lookup connection')

    def _on_connection_state_change(self, evt: ConnectionChangeEvent) -> None:
        print(f'...connection state changed. connected: {evt.connected}, type: {evt.connection_type.name}')

    def _on_state_change(self, evt: StateChangeEvent) -> None:
        match evt.name:
            case StateName.GYROSCOPE_X \
                 | StateName.GYROSCOPE_Y \
                 | StateName.GYROSCOPE_Z \
                 | StateName.L2 \
                 | StateName.R2 \
                 | StateName.ACCELEROMETER_X \
                 | StateName.ACCELEROMETER_Y \
                 | StateName.ACCELEROMETER_Z:
                return
            case _:
                print('_on_state_change', evt.name, evt.new_value)


def main():
    Example()


if __name__ == "__main__":
    main()
