from serial.tools import list_ports

from config import MAX_ROUTE_ID

def parse_company_id(value: str) -> int:
    """
    Convert CLI args from strings -> hex

    e.g.
        "1234"
        "0x1234"
    """

    # Obtain value + convert
    value = value.lower().replace("0x", "")

    # Parse in base 16
    company_id = int(value, 16)

    # Boundary checking
    if not 0 <= company_id <= 0xFFFF:
        raise ValueError("Company ID must fit in 16 bits")

    return company_id

def list_serial_ports():
    """
    List serial ports so the FMA120 port can be identified
    """

    for port in list_ports.comports():
        print(port.device, port.description)

def parse_route_id(value: str) -> int:
    """
    Boundary check the --route arg.
    """

    # Convert to int first
    route_id = int(value, 10)
 
    # Boundary checking
    if not 1 <= route_id <= MAX_ROUTE_ID:
        raise ValueError(f"Route ID must be between 1 and {MAX_ROUTE_ID}")
 
    return route_id
