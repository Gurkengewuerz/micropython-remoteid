from micropython import const

import struct
import ubluetooth

_IRQ_SCAN_RESULT = const(5)


class BluetoothService:
    # bluetooth irq event code

    def __init__(self, callback) -> None:
        self._ble = ubluetooth.BLE()
        self.callback = callback

    def _ble_irq_handler(self, event, data):
        if event == _IRQ_SCAN_RESULT:

            # A single scan result.
            addr_type, addr, adv_type, rssi, adv_data = data

            mac = bytes(addr)
            serviceUUID_lenght = adv_data[0]
            serviceUUID_type = adv_data[1]
            serviceUUID_int = adv_data[2:4]
            serviceUUID_hex = struct.unpack('H', serviceUUID_int)[0]
            serviceData = adv_data[4:]

            self.callback(mac, rssi, serviceUUID_hex, serviceData)

    def start_listening(self) -> None:
        self._ble.irq(self._ble_irq_handler)

        # Scan continuously (at 100% duty cycle)
        self._ble.gap_scan(0, 30000, 30000)

    def start(self):
        # Activate ESP32's Bluetooth module
        while not self._ble.active():
            self._ble.active(True)

    def stop(self):
        while self._ble.active():
            self._ble.active(False)

    def advertise(self, adv):
        self._ble.gap_advertise(500000, adv_data=adv, connectable=False)

