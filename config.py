# Default Route ID when --route is omitted
ROUTE_ID = 1
# Highest Route ID the Broadcast ID layout can have
MAX_ROUTE_ID = 0xFF

# Encryption key, shared by all stops
SHARED_BROADCAST_CODE = "AURAAC_DEMO"

# Two bytes at the front of every payload
MAGIC = b"AU"

# Incremented on any change to the payload layout
PROTOCOL_VERSION = 1

# Unused, reserved
DIRECTION_OUTBOUND = 0
LANGUAGE_ENGLISH = 1