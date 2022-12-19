from .interface import RemoteID_Message

from .auth import RemoteID_Auth
from .system import RemoteID_System
from .selfid import RemoteID_SelfID
from .basicid import RemoteID_BasicID
from .location import RemoteID_Location
from .messagepack import RemoteID_MessagePack
from .operatorid import RemoteID_OperatorID

Header_Type = {
    "RemoteID_BasicID": 0x0,
    "RemoteID_Location": 0x1,
    "RemoteID_Auth": 0x2,
    "RemoteID_SelfID": 0x3,
    "RemoteID_System": 0x4,
    "RemoteID_OperatorID": 0x5,
    "RemoteID_MessagePack": 0xF,
}

class RemoteID_Header(RemoteID_Message):

    def __init__(self) -> None:
        self.remoteid_type = None
        self.version = None
    
    @staticmethod
    def parse(data) -> "RemoteID_Header":
        pack = RemoteID_Header()
        pack.remoteid_type = (data[0] & 0xF0) >> 4
        pack.version = data[0] & 0x0F
        return pack

    def pack(self):
        type_nibble = (self.remoteid_type << 4) & 0xF0
        version_nibble = self.version & 0x0F
        return (type_nibble | version_nibble).to_bytes(1, "little")

    def __str__(self) -> str:
        return f"RemoteID_Header: remoteid_type={self.get_key_from_value(Header_Type, self.remoteid_type)} version={hex(self.version)}"