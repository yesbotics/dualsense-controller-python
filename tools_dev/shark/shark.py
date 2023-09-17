import curses
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from time import sleep
from typing import Final

import _curses

from tools_dev.shark.TSharkCapture import TSharkCapture


class Shark:

    def __init__(self, stdscr: _curses.window, capture_interface_name: str, destination: str):
        self.__stdscr = stdscr
        self.__capture: Final[TSharkCapture] = TSharkCapture(
            interface=capture_interface_name,
            destination=destination
        )
        self.__buff: list[str] | None = []
        self.__last_frame_data: str | None = None

    def __on_data(self, data: str) -> None:
        if 38 <= len(data) <= 53:
            line: str = data[6:]  # cut leading numbers
            self.__buff.append(line)
            if len(self.__buff) == 5:
                single_line: str = " ".join(self.__buff[1:])  # glue lines except first line
                frame_data: str = single_line[33:]  # cut leading numbers
                self.__on_frame_data(frame_data)
                self.__buff.clear()

    def __on_frame_data(self, frame_data: str) -> None:
        if self.__last_frame_data != frame_data:
            self.__on_frame_data_change(
                self.__last_frame_data if self.__last_frame_data is not None else frame_data,
                frame_data
            )
            self.__last_frame_data = frame_data

    def __on_frame_data_change(self, old_data: str | None, new_data: str) -> None:
        # posi: str = "00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47"
        # head: str = "ID|FP|FC|MR|ML|           |ML|MM|TRMTR1TR2  3  4  5  6  7                |TL                              |                       |LO|LS|PO|BR|PL|R |G |B "
        # data: str = "02 0f 55 00 00 00 00 00 00 02 00 05 00 00 00 00 00 00 00 00 00 00 21 c0 03 00 00 d8 36 00 00 00 00 00 00 00 00 00 00 07 01 00 02 00 2a b0 13 55"

        bytez: list[str] = new_data.split(' ')

        @dataclass(frozen=True)
        class Bubs:
            name: str
            indexes: list[int]

        bubse: list[Bubs] = [
            Bubs(name='operating_mode', indexes=[0]),
            Bubs(name='flags_physics', indexes=[1]),
            Bubs(name='flags_controls', indexes=[2]),
            Bubs(name='motor_right', indexes=[3]),
            Bubs(name='motor_left', indexes=[4]),
            Bubs(name='microphone_led', indexes=[9]),
            Bubs(name='microphone_mute', indexes=[10]),
            Bubs(name='right_trigger', indexes=[11, 12, 13, 14, 15, 16, 17, 20]),
            Bubs(name='left_trigger', indexes=[22, 23, 24, 25, 26, 27, 28, 31]),
            Bubs(name='led_options', indexes=[39]),
            Bubs(name='lightbar_pulse_options', indexes=[42]),
            Bubs(name='player_leds_brightness', indexes=[43]),
            Bubs(name='player_leds_enable', indexes=[44]),
            Bubs(name='color', indexes=[45, 46, 47]),
        ]

        self.__stdscr.clear()
        self.__stdscr.addstr(f'{new_data}\n')
        for bubs in bubse:
            self.__stdscr.addstr(f'{bubs.name}: {" ".join([bytez[idx] for idx in bubs.indexes])}\n')

        self.__stdscr.refresh()

    def run(self) -> None:
        self.__capture.sniff(self.__on_data)
        while True:
            sleep(0.0000000001)


def main(stdscr: _curses.window):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input

    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("capture_interface_name")
    parser.add_argument("destination")
    args: Namespace = parser.parse_args()

    Shark(
        stdscr,
        capture_interface_name=args.capture_interface_name,
        destination=args.destination,
    ).run()


if __name__ == "__main__":
    curses.wrapper(main)
