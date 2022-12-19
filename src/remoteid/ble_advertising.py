from micropython import const
import struct
import ubluetooth

# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)
_ADV_TYPE_SERVICE_DATA = const(0x16)


def advertising_payload(limited_disc=False, br_edr=False, name=None, uuid=None, appearance=0,service_data=None):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    #if uuid:
    #    b = bytes(uuid)
    #    if len(b) == 2:
    #        _append(_ADV_TYPE_UUID16_COMPLETE, b)
    #    elif len(b) == 4:
    #        _append(_ADV_TYPE_UUID32_COMPLETE, b)
    #    elif len(b) == 16:
    #        _append(_ADV_TYPE_UUID128_COMPLETE, b)

    #_append(
    #    _ADV_TYPE_FLAGS,
    #    struct.pack("B", (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04)),
    #)

    #if name:
    #    _append(_ADV_TYPE_NAME, name)

    if service_data:
        if uuid:
            b = bytes(uuid)
            service_data = b + service_data
        _append(_ADV_TYPE_SERVICE_DATA, service_data)

    # See org.bluetooth.characteristic.gap.appearance.xml
    #if appearance:
    #    _append(_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

    return payload
