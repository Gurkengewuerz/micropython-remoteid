from .interface import RemoteID_Message, MAX_AUTH_DATA, MAX_AUTH_DATA_PAGES, MAX_AUTH_PAGE_NON_ZERO_SIZE, MAX_AUTH_PAGE_ZERO_SIZE
import ubinascii
import struct

class RemoteID_Auth(RemoteID_Message):

    def __init__(self, auth_type, auth_data_page, auth_last_page_index, auth_length, auth_timestamp, auth_data) -> None:
        self.auth_type = auth_type
        self.auth_data_page = auth_data_page
        self.auth_last_page_index = auth_last_page_index
        self.auth_length = auth_length
        self.auth_timestamp = auth_timestamp
        self.auth_data = auth_data
    
    @staticmethod
    def parse(data) -> "RemoteID_Auth":
        pack = RemoteID_Auth(None, None, None, None, None, None)
        types = data[0]
        pack.auth_type = (types & 0xF0) >> 4
        pack.auth_data_page = types & 0x0F
        pack.auth_data = [0x00] * MAX_AUTH_DATA
        data = data[1:]

        offset = 0
        amount = MAX_AUTH_PAGE_ZERO_SIZE
        if pack.auth_data_page:
            next_format = "<BBi"
            next_size = struct.calcsize(next_format)
            lpi, length, ts = struct.unpack(next_format, data[:next_size])
            data = data[next_size:]

            pack.auth_last_page_index = lpi
            pack.auth_length = length
            pack.auth_timestamp = ts

            x = pack.auth_last_page_index * MAX_AUTH_PAGE_NON_ZERO_SIZE + MAX_AUTH_PAGE_ZERO_SIZE
            if pack.auth_last_page_index >= MAX_AUTH_DATA_PAGES or pack.auth_length > x:
                pack.auth_last_page_index = 0
                pack.auth_length = 0
                pack.auth_timestamp = 0
            else:
                pack.auth_length = len
        else:
            offset = MAX_AUTH_PAGE_ZERO_SIZE + (pack.auth_data_page - 1) * MAX_AUTH_PAGE_NON_ZERO_SIZE
            amount = MAX_AUTH_PAGE_NON_ZERO_SIZE

        if pack.auth_data_page >= 0 and pack.auth_data_page < MAX_AUTH_DATA_PAGES:
            cnt = 0
            for i in range(offset, offset + amount):
                pack.auth_data[i] = data[cnt]
                cnt += 1
            pack.auth_data_str = ubinascii.hexlify(pack.auth_data)
        return pack

    def pack(self):
        pass
    
    def __str__(self) -> str:
        return f"RemoteID_Auth: auth_type={self.auth_type} auth_data_page={self.auth_data_page} auth_last_page_index={self.auth_last_page_index} auth_length={self.auth_length} auth_timestamp={self.auth_timestamp} auth_data={self.auth_data}"