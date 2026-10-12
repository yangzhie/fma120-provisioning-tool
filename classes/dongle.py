
import re
import time
import serial

from classes.stop import Stop
from utils.formatting import build_bf_hex
from config import SHARED_BROADCAST_CODE


class FMA120:
    """
    Control FMA120 and FMA121 transmitters
    through their USB serial interfaces.
    """

    def __init__(self, port: str):
        """
        Open the transmitter's serial connection.

        Examples:
            COM8
            8 -> automatically converted to COM8
            /dev/ttyACM0
        """

        port = str(port).strip()

        # Convert Windows port numbers to COM names
        if port.isdigit():
            port = f"COM{port}"

        # Normalize COM port spelling
        if re.fullmatch(r"com\d+", port, re.IGNORECASE):
            port = port.upper()

        self.port = port

        print(f"Connecting to transmitter on {self.port}")

        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=921600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=2,
                write_timeout=2
            )

        except serial.SerialException as error:
            raise RuntimeError(
                f"Cannot open serial port {self.port}. "
                "Check the COM port in Device Manager, "
                "make sure the transmitter is connected, "
                "and close FlooCast or other programs "
                "using the port."
            ) from error

        # Allow device to settle
        time.sleep(0.3)

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        print(f"Connected successfully to {self.port}")

    def close(self):
        """
        Close the serial connection.
        """

        if self.ser.is_open:
            self.ser.close()
            print(f"Disconnected from {self.port}")

    def command(self, body: str) -> list[str]:
        """
        Send a BAI command to the transmitter.

        Format:
            BC:<command>\\r\\n
        """

        packet = f"BC:{body}\r\n".encode("ascii")

        print(f"TX  BC:{body}")

        self.ser.write(packet)
        self.ser.flush()

        responses = []

        while True:
            raw = self.ser.readline()

            if not raw:
                break

            text = raw.decode(
                "ascii",
                errors="replace"
            ).strip()

            if text:
                print(f"RX  {text}")
                responses.append(text)

        return responses

    def require_ok(self, body: str):
        """
        Send a command and require an OK response.
        """

        responses = self.command(body)

        if "OK" not in responses:
            raise RuntimeError(
                f"No OK response for BC:{body}. "
                f"Received: {responses}"
            )

    def provision(self, stop: Stop, company_id: int):
        """
        Configure FMA120 or FMA121 as a Route 86 stop.

        BN = Broadcast Name
        BE = Broadcast Encryption Code
        BI = Broadcast ID
        BF = Route / Stop Metadata
        """

        print("\n================================")
        print("Auracast Transmitter Provisioning")
        print("================================")

        print(f"Serial Port: {self.port}")
        print(f"Stop Number: {stop.index}")
        print(f"Broadcast Name: {stop.broadcast_name}")
        print(f"Broadcast ID: {stop.broadcast_id}")

        bf = build_bf_hex(stop, company_id)

        # Set broadcast name
        self.require_ok(
            f"BN={stop.broadcast_name}"
        )

        # Set shared broadcast code
        self.require_ok(
            f"BE={SHARED_BROADCAST_CODE}"
        )

        # Set unique broadcast ID
        self.require_ok(
            f"BI={stop.broadcast_id}"
        )

        # Set Route 86 metadata
        self.require_ok(
            f"BF={bf}"
        )

        print("\nVerification:")

        self.command("BN")
        self.command("BI")
        self.command("BF")

        print("\nProvisioning commands completed.")


# Optional descriptive alias for newer code
FMATransmitter = FMA120
