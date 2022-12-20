from .messages.auth import RemoteID_Auth
from .messages.system import RemoteID_System
from .messages.selfid import RemoteID_SelfID
from .messages.basicid import RemoteID_BasicID
from .messages.header import RemoteID_Header, Header_Type
from .messages.location import RemoteID_Location
from .messages.messagepack import RemoteID_MessagePack
from .messages.operatorid import RemoteID_OperatorID

from .ble import BluetoothService
from .ble_advertising import advertising_payload

import ubluetooth
import gc
import time

class RemoteIDPayload:

    def __init__(self, msg_counter, timestamp, header, payload) -> None:
        self.msg_counter = msg_counter
        self.timestamp = timestamp
        self.header = header
        self.payload = payload

    def pack(self):
        a = (0x0D).to_bytes(1, "little")
        b = self.msg_counter.to_bytes(1, "little")
        c = self.header.pack()
        d = self.payload.pack()

        return a + b + c + d

    def __str__(self) -> str:
        return f""


RemoteIDManager_Mode = {
    "LISTEN": 0x0,
    "SEND": 0x1,
    "STOP": 0xFF
}

class RemoteIDManager:

    def __init__(self) -> None:
        self.ble_service = BluetoothService(self.receive_bluetooth)

        self.mode = None

        self._queue = {}
        self._message_counter = 0
        self._last_send = 0
        self._last_idx = 0
    
    def set_mode(self, mode):
        self.mode = mode
        self.ble_service.stop()
        if mode == RemoteIDManager_Mode["LISTEN"]:
            self.ble_service.start()
            self.ble_service.start_listening()
        elif mode == RemoteIDManager_Mode["SEND"]:
            self.ble_service.start()

    def receive_bluetooth(self, mac, rssi, short_service_uuid, data) -> None:
        if short_service_uuid != 0xFFFA:
            return

        application_code = data[0]
        msg_counter = data[1]
        data = data[2:]
        
        if application_code != 0x0D:
            return
        
        header_data = [data[0]]
        header = RemoteID_Header.parse(header_data)

        data = data[1:]
        payload = RemoteIDPayload(msg_counter, time.ticks_ms(), header, None)

        func = None
        if header.remoteid_type == Header_Type[RemoteID_BasicID.__class__.__name__]:
            func = RemoteID_BasicID.parse
        elif header.remoteid_type == Header_Type[RemoteID_Location.__class__.__name__]:
            func = RemoteID_Location.parse
        elif header.remoteid_type == Header_Type[RemoteID_Auth.__class__.__name__]:
            func = RemoteID_Auth.parse
        elif header.remoteid_type == Header_Type[RemoteID_SelfID.__class__.__name__]:
            func = RemoteID_SelfID.parse
        elif header.remoteid_type == Header_Type[RemoteID_System.__class__.__name__]:
            func = RemoteID_System.parse
        elif header.remoteid_type == Header_Type[RemoteID_OperatorID.__class__.__name__]:
            func = RemoteID_OperatorID.parse
        elif header.remoteid_type == Header_Type[RemoteID_MessagePack.__class__.__name__]:
            func = RemoteID_MessagePack.parse
        else:
            print("Received unknown type", header.remoteid_type)
        
        if data is not None:
            payload.payload = func(data)

        if payload.payload is None:
            return
        
        print(payload.payload)
        gc.collect()

    def queue_add(self, message):
        self._queue[message.__class__.__name__] = message

    def queue_remove(self, message):
        del self._queue[message.__class__.__name__]

    def send_bluetooth(self):
        if self.mode != RemoteIDManager_Mode["SEND"]:
            return
        
        now = time.ticks_ms()

        spacing_ms = 250
        if now - self._last_send < spacing_ms:
            return

        if self._message_counter >= 0xFF:
            self._message_counter = 0x00
        
        keys = list(self._queue.keys())
        max_keys = len(keys)
        if max_keys == 0:
            return
        
        if self._last_idx + 1 < max_keys:
            self._last_idx += 1
        else:
            self._last_idx = 0
            self._message_counter += 1

        msg = self._queue[keys[self._last_idx]]
        header = RemoteID_Header()

        header.remoteid_type = Header_Type[msg.__class__.__name__]
        header.version = 0x01
        data = RemoteIDPayload(self._message_counter, 0, header, msg).pack()

        payload = advertising_payload(
            service_data=data, uuid=ubluetooth.UUID(0xFFFA)
        )
        #print(msg.__class__.__name__, len(data), len(payload), ubinascii.hexlify(payload).upper())

        self.ble_service.advertise(payload)

        self._last_send = now
        gc.collect()