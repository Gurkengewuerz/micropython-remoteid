from .interface import RemoteID_Message, MAX_ID_BYTE_SIZE

BasicID_ID_Type = {
    "NONE": 0,
    "SERIAL_NUMBER": 1,
    "CAA_REGISTRATION_ID": 2,
    "UTM_ASSIGNED_UUID": 3,
    "SPECIFIC_SESSION_ID": 4
}

BasicID_UA_Type = {
    "NONE": 0,
    "AEROPLANE": 1,
    "HELICOPTER_OR_MULTIROTOR": 2,
    "GYROPLANE": 3,
    "HYBRID_LIFT": 4,
    "ORNITHOPTER": 5,
    "GLIDER": 6,
    "KITE": 7,
    "FREE_BALLOON": 8,
    "CAPTIVE_BALLOON": 9,
    "AIRSHIP": 10,
    "FREE_FALL_PARACHUTE": 11,
    "ROCKET": 12,
    "TETHERED_POWERED_AIRCRAFT": 13,
    "GROUND_OBSTACLE": 14,
    "OTHER": 15
}


class RemoteID_BasicID(RemoteID_Message):

    def __init__(self) -> None:
        self.id_type = 0xF
        self.ua_type = 0xF
        self.uas_id = ""

    @staticmethod
    def parse(data) -> "RemoteID_BasicID":
        pack = RemoteID_BasicID()
        basic_types = data[0]
        pack.id_type = (basic_types & 0xF0) >> 4
        pack.ua_type = basic_types & 0x0F
        pack.uas_id = str(data[1:], 'ascii')
        return pack

    def pack(self):
        id_type_nibble = (self.id_type << 4) & 0xF0
        ua_type_nibble = self.ua_type & 0x0F
        basic_types = (id_type_nibble | ua_type_nibble).to_bytes(1, "little")

        uas_id = bytes(self.uas_id, "ascii")
        uas_id += b"\0" * (MAX_ID_BYTE_SIZE - len(uas_id))

        return basic_types + uas_id + (b"\0" * 3)

    def __str__(self) -> str:
        return f"RemoteID_BasicID: id_type={self.get_key_from_value(BasicID_ID_Type, self.id_type)} ua_type={self.get_key_from_value(BasicID_UA_Type, self.ua_type)} uas_id=\"{self.uas_id}\""
