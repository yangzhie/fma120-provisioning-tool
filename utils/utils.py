
import time

from classes.stop import Stop


def list_audio_devices():
    """
    List available computer audio output devices.

    FMA120:
        Select the FMA120 USB audio output.

    FMA121:
        Select the computer headphone/speaker output
        connected to the FMA121 3.5mm audio input.

        Alternatively, select FMA121 USB audio if
        USB Audio Input is enabled in FlooCast.
    """

    import pygame
    from pygame._sdl2 import audio as sdl2_audio

    # Initialize pygame for device discovery
    pygame.init()

    try:
        # False means output devices
        devices = sdl2_audio.get_audio_device_names(False)

        print("\nAvailable audio output devices:")
        print("--------------------------------")

        if not devices:
            print("No audio output devices found.")
            return

        for index, name in enumerate(devices):
            print(f"[{index}] {name}")

    finally:
        pygame.quit()


def play_audio(
    stop: Stop,
    audio_device: str | None,
    once: bool = False,
    audio_input: str = "usb"
):
    """
    Play an audio announcement for a selected stop.

    Supported audio configurations:

    1. FMA120 - USB
       Computer -> USB audio -> FMA120 -> Auracast

    2. FMA121 - AUX
       Computer -> 3.5mm cable -> FMA121 -> Auracast

    3. FMA121 - USB
       Computer -> USB audio -> FMA121 -> Auracast
       (Requires USB Audio Input enabled in FlooCast)

    Parameters:
        stop:
            Stop object containing the audio file path.

        audio_device:
            Name of the computer audio output device.

        once:
            True = play the announcement once.
            False = continuously loop the announcement.

        audio_input:
            "usb" = USB audio configuration.
            "aux" = 3.5mm audio configuration.
    """

    import pygame



    if audio_input not in ("usb", "aux"):
        raise ValueError(
            "Invalid audio input. Choose 'usb' or 'aux'."
        )



    if audio_input == "usb":

        if not audio_device:
            raise ValueError(
                "USB audio requires an audio device. "
                "Use 'python main.py list-audio' to find "
                "the FMA120/FMA121 USB audio output."
            )

    elif audio_input == "aux":

        if not audio_device:
            raise ValueError(
                "AUX audio requires a computer audio output. "
                "Use 'python main.py list-audio' to find "
                "the headphone/speaker output connected "
                "to the FMA121 3.5mm input."
            )



    audio_file = stop.audio_path

    if not audio_file.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_file}"
        )



    print("\n================================")
    print("Auracast Audio Playback")
    print("================================")

    print(f"Stop: {stop.index}")
    print(f"Audio file: {audio_file}")
    print(f"Audio input mode: {audio_input}")
    print(f"Computer output device: {audio_device}")

    if audio_input == "usb":

        print("Connection: USB Audio")
        print(
            "Make sure the transmitter's USB "
            "audio input is enabled."
        )

    elif audio_input == "aux":

        print("Connection: 3.5mm AUX")
        print(
            "Make sure the computer audio output "
            "is connected to the FMA121 3.5mm jack."
        )
        print(
            "The FMA121 USB-C connection supplies "
            "power and serial communication."
        )



    # Stop previous mixer session
    pygame.mixer.quit()

    try:

        pygame.mixer.init(
            frequency=48000,
            size=-16,
            channels=2,
            buffer=1024,
            devicename=audio_device
        )


        pygame.mixer.music.load(
            str(audio_file)
        )



        if once:
            pygame.mixer.music.play(0)
            print("\nPlayback mode: Play once")

        else:
            pygame.mixer.music.play(-1)
            print("\nPlayback mode: Continuous loop")

        print("Audio playback started.")
        print("Press Ctrl+C to stop.")



        while pygame.mixer.music.get_busy():
            time.sleep(0.25)

    except KeyboardInterrupt:

        print("\nAudio playback stopped by user.")

    finally:


        pygame.mixer.music.stop()
        pygame.mixer.quit()

        print("Audio resources released.")
