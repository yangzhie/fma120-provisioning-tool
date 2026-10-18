# FMA120 Provisioning TOol
Provisions FlooGoo FMA120/FMA121 transmitters and broadcasts their announcements over Auracast.

Part of the [Auracast Companion](https://github.com/yangzhie/auracast-companion) proof-of-concept. It is a system that automatically connects hard-of-hearing riders' broadcast sinks (headphones, hearing aids, etc.) to the right broadcast at each stop of a journey. The companion application discovers these provisioned broadcasts and joins them.
## Purpose
Provisions a FMA120/FMA121 transmitter to become one public transport stop. Takes two separate things:

**Configuration**: written to the dongle over USB serial and persists in its memory.

**Audio**: audio source has to be keep fed the dongle for as long as the stop is live.
## Requirements
- Python 3.10+
- FMA120 firmware (1.1.6.7+)
- A FMA120/FMA121 connected over USB

```bash
pip install pyserial pygame
```
## Usage
1. Find the dongle's serial port: `python main.py list-ports`
2. Provision the dongle: `python main.py provision --stop <number> --port <port(/dev/tty/<> // COM)> --company-id FFFF`
3. Start broadcasting: `python main.py play --stop <stop>`

Note: Windows uses `COM<number>`, Linux uses `/dev/tty/<ACM>`
## Commands
- `list-ports`: Find which serial port the FMA120/FMA121 is on while plugged in.
- `provision`: Write configuration to one dongle.
- `play`: Loop a stop's announcement through the dongle.
## Audio files
Expected file types: `.mp3`, `.mp4`, `.wav`
## Dongle Configuration
Four BAI commands, sent over serial as `BC:<command>\r\n`:
- `BN` - `AURA86-S1` - Broadcast name, shown in the phone's Auracast picker.
- `BE` - `AURA86DEMO2026` - Broadcast code (encryption key, all stops share this).
- `BI` - `560001` - Standard Auracast Broadcast ID.
- `BF` - `0CFFFFFF415501560001000101` - Custom route/stop metadata.
## BF Metadata Layout
`BF` carries the custom data Android Companion matches on. It's standard BLE manufacturer-specific data wrapping a 9-byte project payload.

```
0C          length — 12 bytes
FF          AD type — manufacturer-specific data
FF FF       company ID, little-endian (0xFFFF = reserved for testing)
41 55       "AU" magic — identifies this project
01          protocol version
56 00       route ID (86), little-endian uint16
01          stop index
00          direction (0 = outbound)
01          language (1 = English)
01          audio ID
```