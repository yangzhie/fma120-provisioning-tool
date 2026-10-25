#!/usr/bin/env python3
from __future__ import annotations
import argparse

from classes.dongle import *
from classes.stop import *
from utils.audio import *
from utils.formatting import *
from utils.utils import *

from config import (
    ROUTE_ID,
    SHARED_BROADCAST_CODE,
    MAGIC,
    PROTOCOL_VERSION
)

# Dedicated/hard-coded stops dictionary for the proof-of-concept
STOPS = {
    1: Stop(
        index=1,
        name="Stop 1",
        folder="Stop1",
        audio_stem="audio1"
    ),
    2: Stop(
        index=2,
        name="Stop 2",
        folder="Stop2",
        audio_stem="audio2"
    ),
    3: Stop(
        index=3,
        name="Stop 3",
        folder="Stop3",
        audio_stem="audio3"
    ),
    4: Stop(
        index=4,
        name="Stop 4",
        folder="Stop4",
        audio_stem="audio4"
    )
}

def main():
    """
    Driver function, CLI entry point.

    Commands:
        list-ports
        provision
        play
    """

    # Parser-architecture
    parser = argparse.ArgumentParser(description="Auracast FMA120 proof-of-concept controller")
    # Register each command
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    # Find which port the FMA120 is on
    subparsers.add_parser("list-ports", help="List available serial ports")

    # Print all stops' config and BF hex
    show_spec = subparsers.add_parser("show-spec", help="Show metadata for all Route 86 stops")
    show_spec.add_argument("--company-id", required=True, help="Bluetooth Company ID in hexadecimal")

    # Write config to FMA120
    provision = subparsers.add_parser("provision", help="Configure an FMA120 for a selected stop")
    provision.add_argument("--port", required=True, help="Serial / COM port of the FMA120")
    provision.add_argument("--stop", type=int, choices=range(1, 5), required=True, help="Stop number from 1 to 4")
    provision.add_argument("--company-id", required=True, help="Bluetooth Company ID in hexadecimal")

    # Loop a stop's audio
    play = subparsers.add_parser("play", help="Play the audio announcement for a selected stop")
    play.add_argument("--stop", type=int, choices=range(1, 5), required=True, help="Stop number from 1 to 4")

    # Dispatching: each branch pulls what it needs out of args and calls the relevant function
    args = parser.parse_args()
    if args.cmd == "list-ports":
        list_serial_ports()
    elif args.cmd == "provision":
        stop = STOPS[args.stop]
        company_id = parse_company_id(args.company_id)
        device = FMA120(args.port)
        try:
            device.provision(stop, company_id)
        finally:
            device.close()
    elif args.cmd == "play":
        play_audio(STOPS[args.stop], args.audio_device)

if __name__ == "__main__":
    """
    Main dunder
    """

    main()