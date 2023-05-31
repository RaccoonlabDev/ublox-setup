# ublox-setup

Setup U-Blox module to work with RaccoonLab devices.

More details you can found on the [U-Blox module setup instructions](https://docs.raccoonlab.co/guide/gps_mag_baro/ublox_setup.html).

## Prerequisites

You need a USB-serial converter. Connect the device with RaccoonLab GNSS via UART connector.

## Install

```bash
pip install -r requirements.txt
```

## Usage example

Windows:

```bash
python3 ubx.py
```

Ubuntu:

```bash
./ubx.py -s /dev/ttyACM0
```
