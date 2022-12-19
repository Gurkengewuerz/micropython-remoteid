from .interface import RemoteID_Message, MAX_MESSAGE_SIZE, MAX_MESSAGES_IN_PACK


class RemoteID_MessagePack(RemoteID_Message):

    def __init__(self) -> None:
        self.message_size = 0
        self.messages_in_pack = 0
        self.messages = []

    @staticmethod
    def parse(data) -> "RemoteID_MessagePack":
        pack = RemoteID_MessagePack()

        pack.message_size = data[0]
        pack.messages_in_pack = data[1]

        if pack.message_size != MAX_MESSAGE_SIZE or pack.messages_in_pack <= 0 or pack.messages_in_pack > MAX_MESSAGES_IN_PACK:
            return None
        
        data = data[2:]
        pack.messages = data
        return pack 

    def pack(self):
        pass

    def __str__(self) -> str:
        return f"RemoteID_MessagePack: message_size={self.message_size} messages_in_pack={self.messages_in_pack}"
