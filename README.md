# RemoteID Transceiver
This repository provides a micropython library for encoding and decoding Open Drone ID messages, as the format is defined in the ASTM F3411 Remote ID and the ASD-STAN prEN 4709-002 Direct Remote ID specifications.

## Development Setup
1. Clone the newest [micropython-stubs](https://github.com/Josverl/micropython-stubs) 
2. Create a symbolic link names `stubs` to the `stubs/` directory of `Josverl/micropython-stubs`. See [here](https://micropython-stubs.readthedocs.io/en/latest/40_symlink.html#create-symbolic-link) for help.
3. Use VSCode with PyMakr extension

## TODO
- Currently only BLE Advertising is supported. To allow WiFi Beacons a [C module](https://forum.micropython.org/viewtopic.php?f=3&t=11756&p=64028&hilit=promiscuous#p64028) must be written.