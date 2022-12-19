LAT_LONG_MULTIPLIER = 1e-7
SPEED_VERTICAL_MULTIPLIER = 0.5

MAX_AUTH_DATA_PAGES = 16
MAX_AUTH_PAGE_ZERO_SIZE = 17
MAX_AUTH_PAGE_NON_ZERO_SIZE = 23
MAX_AUTH_DATA = MAX_AUTH_PAGE_ZERO_SIZE + (MAX_AUTH_DATA_PAGES - 1) * MAX_AUTH_PAGE_NON_ZERO_SIZE

MAX_MESSAGE_SIZE = 25
MAX_MESSAGES_IN_PACK = 9

MAX_ID_BYTE_SIZE = 20
MAX_STRING_BYTE_SIZE = 23

class RemoteID_Message:
    
    def get_key_from_value(self, d, val):
        keys = [k for k, v in d.items() if v == val]
        if keys:
            return keys[0]
        return val
    
    def pack(self):
        pass