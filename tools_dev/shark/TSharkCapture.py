import subprocess
from subprocess import Popen
from threading import Thread, Event
from typing import Final, Callable


class TSharkCapture:

    def __init__(self, interface: str, destination: str):
        self.__interface: Final[str] = interface
        self.__destination: Final[str] = destination
        self.__capture_thread: Thread | None = None
        self.__stop_event: Final[Event] = Event()

    def sniff(self, callback: Callable[[str], None]) -> None:
        self.__stop_event.clear()
        self.__capture_thread = Thread(target=self._sniff, daemon=True, args=(callback,))
        self.__capture_thread.start()

    def stop(self) -> None:
        self.__stop_event.set()
        self.__capture_thread.join()
        self.__capture_thread = None

    def _sniff(self, callback: Callable[[str], None]) -> None:
        cmd: str = 'tshark' \
                   f' -i {self.__interface}' \
                   f' -Y "usb.dst == {self.__destination}"' \
                   ' --hexdump frames' \
                   ' --hexdump delimit' \
                   ' --hexdump noascii'
        process: Popen[str] = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while not self.__stop_event.is_set():
            output: str = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                callback(output.strip())
        process.kill()
