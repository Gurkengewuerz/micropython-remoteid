from .interface import RemoteID_Message, MAX_STRING_BYTE_SIZE


SelfID_Description_Type = {
    "TEXT": 0,
    "EMERGENCY": 1,
    "EXTENDED_STATUS": 2
}

class RemoteID_SelfID(RemoteID_Message):

    def __init__(self) -> None:
        self.description_type = 0xFF
        self.operation_description = ""
    
    @staticmethod
    def parse(data) -> "RemoteID_SelfID":
        pack = RemoteID_SelfID()
        pack.description_type = data[0]
        pack.operation_description = str(data[1:], 'ascii')
        return pack
    
    def pack(self):
        desc_type = (self.description_type & 0xFF).to_bytes(1, "little")

        desc = bytes(self.operation_description, "ascii")
        desc += b"\0" * (MAX_STRING_BYTE_SIZE - len(desc))
    
        return desc_type + desc

    def __str__(self) -> str:
        return f"RemoteID_SelfID: description_type={self.get_key_from_value(SelfID_Description_Type, self.description_type)} operation_description=\"{self.operation_description}\""