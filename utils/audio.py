import time
import pygame

from classes.stop import Stop

def play_audio(stop: Stop, audio_device: str | None = None):
    """
    Play the audio file associated with a stop.
    Selected audio output should be FMA120 transmitter.

    Flow: audio file -> pygame -> FMA USB device -> FMA120 transmitter -> Auracast broadcast
    """

    # Obtain audio file for the stop
    audio_file = stop.audio_path

    # Stop if audio file does not exist
    if not audio_file.exists():
        raise FileNotFoundError(audio_file)

    # Reset existing mixer session before selecting new output
    pygame.mixer.quit()

    # Initialise output
    pygame.mixer.init(
        frequency=48000,
        size=-16,
        channels=2,
        buffer=1024,
        devicename=audio_device
    )

    # Load stop announcement
    pygame.mixer.music.load(str(audio_file))

    # Play loop
    pygame.mixer.music.play(-1)

    print(f"Playing {audio_file} -> {audio_device or 'default output'}")
    print("Terminate to stop")

    try:
        # Block until interrupted
        while (pygame.mixer.music.get_busy()):
            time.sleep(0.25)
    except KeyboardInterrupt:
        # Stop playback (terminate w/ Ctrl+C)
        pass
    finally:
        # Clean up mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()

