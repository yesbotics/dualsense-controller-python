from time import sleep

from dualsense_controller import DualSenseController, EventType, Event


class Example:
    def __init__(self):
        self._dsc: DualSenseController = DualSenseController(0)
        self._dsc.add_event_listener(EventType.CONNECTION_LOOKUP, self._on_connection_lookup)
        self._dsc.add_event_listener(EventType.CONNECTION_STATE_CHANGE, self._on_connection_state_change)
        self._dsc.add_event_listener(EventType.VALUE_CHANGE, self._on_value_change)

    def run(self) -> None:
        self._dsc.init()
        sleep(100)

    def _on_connection_lookup(self, evt: Event) -> None:
        print('_on_connection_lookup', evt)

    def _on_connection_state_change(self, evt: Event) -> None:
        print('_on_connection_state_change', evt)

    def _on_value_change(self, evt: Event) -> None:
        print('_on_value_change', evt)


def main():
    example: Example = Example()
    example.run()


if __name__ == "__main__":
    main()
