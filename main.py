
#!/usr/bin/env python3
from __future__ import annotations

import argparse

from classes.dongle import FMATransmitter
from classes.stop import Stop
from utils.audio import list_audio_devices, play_audio
from utils.formatting import build_bf_hex, decode_bf_hex
from utils.utils import list_serial_ports, parse_company_id

from config import (
    ROUTE_ID,
    SHARED_BROADCAST_CODE,
    MAGIC,
    PROTOCOL_VERSION
)


# Route 86 - Four Stop Configuration
STOPS = {
    1: Stop(
        index=1,
        name="Stop 1",
        folder="Stop 1",
        audio_stem="audio1"
    ),
    2: Stop(
        index=2,
        name="Stop 2",
        folder="Stop 2",
        audio_stem="audio2"
    ),
    3: Stop(
        index=3,
        name="Stop 3",
        folder="Stop 3",
        audio_stem="audio3"
    ),
    4: Stop(
        index=4,
        name="Stop 4",
        folder="Stop 4",
        audio_stem="audio4"
    )
}


def main():
    """
    Route 86 Auracast controller.

    Supports:
        FMA120 - USB audio
        FMA121 - USB or 3.5mm AUX audio

    Commands:
        list-ports
        list-audio
        show-spec
        provision
        play
        run-stop
    """

    parser = argparse.ArgumentParser(
        description=(
            "Route 86 Auracast FMA120/FMA121 "
            "proof-of-concept controller"
        )
    )

    subparsers = parser.add_subparsers(
        dest="cmd",
        required=True
    )

    # ----------------------------------------
    # List available serial ports
    # ----------------------------------------
    subparsers.add_parser(
        "list-ports",
        help="List available USB serial ports"
    )


    subparsers.add_parser(
        "list-audio",
        help="List available audio output devices"
    )


    show_spec = subparsers.add_parser(
        "show-spec",
        help="Show metadata for all Route 86 stops"
    )

    show_spec.add_argument(
        "--company-id",
        required=True,
        help="Bluetooth Company ID in hexadecimal"
    )


    provision = subparsers.add_parser(
        "provision",
        help="Configure an FMA120/FMA121 transmitter"
    )

    provision.add_argument(
        "--port",
        required=True,
        help="Serial / COM port of the transmitter"
    )

    provision.add_argument(
        "--stop",
        type=int,
        choices=range(1, 5),
        required=True,
        help="Stop number from 1 to 4"
    )

    provision.add_argument(
        "--company-id",
        required=True,
        help="Bluetooth Company ID in hexadecimal"
    )

    # ----------------------------------------
    # Play stop audio
    # ----------------------------------------
    play = subparsers.add_parser(
        "play",
        help="Play audio for a selected stop"
    )

    play.add_argument(
        "--stop",
        type=int,
        choices=range(1, 5),
        required=True,
        help="Stop number from 1 to 4"
    )

    play.add_argument(
        "--audio-device",
        help="Computer audio output device"
    )

    play.add_argument(
        "--once",
        action="store_true",
        help="Play once instead of looping"
    )

    # ----------------------------------------
    # Configure transmitter and play audio
    # ----------------------------------------
    run_stop = subparsers.add_parser(
        "run-stop",
        help="Configure transmitter and play stop audio"
    )

    run_stop.add_argument(
        "--port",
        required=True,
        help="Serial / COM port of the transmitter"
    )

    run_stop.add_argument(
        "--stop",
        type=int,
        choices=range(1, 5),
        required=True,
        help="Stop number from 1 to 4"
    )

    run_stop.add_argument(
        "--company-id",
        required=True,
        help="Bluetooth Company ID in hexadecimal"
    )

    run_stop.add_argument(
        "--audio-device",
        help="Computer audio output device"
    )


    for audio_command in (play, run_stop):

        audio_command.add_argument(
            "--audio-input",
            choices=("usb", "aux"),
            default="usb",
            help=(
                "usb: send audio to transmitter USB "
                "audio output; "
                "aux: send audio to the computer output "
                "wired to FMA121 3.5mm input"
            )
        )


    args = parser.parse_args()

    if args.cmd == "list-ports":
        list_serial_ports()

    elif args.cmd == "list-audio":
        list_audio_devices()

    elif args.cmd == "show-spec":

        company_id = parse_company_id(
            args.company_id
        )

        for stop in STOPS.values():

            bf = build_bf_hex(
                stop,
                company_id
            )

            print("\n==========================")
            print(f"Stop: {stop.index}")
            print(f"Name: {stop.name}")
            print(f"Broadcast Name: {stop.broadcast_name}")
            print(f"Broadcast Code: {SHARED_BROADCAST_CODE}")
            print(f"Broadcast ID: {stop.broadcast_id}")
            print(f"BF: {bf}")
            print(f"Decoded BF: {decode_bf_hex(bf)}")
            print(f"Audio File: {stop.audio_path}")

    elif args.cmd == "provision":

        stop = STOPS[args.stop]

        company_id = parse_company_id(
            args.company_id
        )

        device = FMATransmitter(
            args.port
        )

        try:
            device.provision(
                stop,
                company_id
            )

        finally:
            device.close()

    elif args.cmd == "play":

        play_audio(
            STOPS[args.stop],
            args.audio_device,
            args.once,
            args.audio_input
        )

    elif args.cmd == "run-stop":

        stop = STOPS[args.stop]

        company_id = parse_company_id(
            args.company_id
        )

        device = FMATransmitter(
            args.port
        )

        try:
            device.provision(
                stop,
                company_id
            )

        finally:
            device.close()

        play_audio(
            stop,
            args.audio_device,
            audio_input=args.audio_input
        )


if __name__ == "__main__":
    main()
