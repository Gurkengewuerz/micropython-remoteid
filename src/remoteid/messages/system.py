from .interface import RemoteID_Message, LAT_LONG_MULTIPLIER
import struct

System_Operator_Location_Type = {
    "TAKEOFF": 0,
    "LIVE_GNSS": 1,
    "FIXED": 2
}

System_Classification_Type = {
    "NONE": 0,
    "EU": 1,
}

System_Category = {
    "NONE": 0,
    "OPEN": 1,
    "SPECIFIC": 2,
    "CERTIFIED": 3,
}

System_Class = {
    "NONE": 0,
    "CLASS_0": 1,
    "CLASS_1": 2,
    "CLASS_2": 3,
    "CLASS_3": 4,
    "CLASS_4": 5,
    "CLASS_5": 6,
    "CLASS_6": 7,
}

class RemoteID_System(RemoteID_Message):

    def __init__(self) -> None:
        self.operator_location_type = System_Operator_Location_Type["TAKEOFF"]
        self.classification_type = System_Classification_Type["NONE"]
        self.latitude = 51.549999
        self.longitude = 7.216667
        self.area_count = 0
        self.area_radius = 0
        self.area_ceiling = 0
        self.area_floor = 0
        self.category = System_Category["NONE"]
        self.class_value = System_Class["NONE"]
        self.altitude_geodetic = 0
        self.system_timestamp = 0

    @staticmethod
    def parse(data) -> "RemoteID_System":
        pack = RemoteID_System()
        
        next_format = "<BiiHBHHBHI"
        next_size = struct.calcsize(next_format)
        types, lat, lng, a_count, a_radius, a_ceil, a_floor, cat, alt_geo, ts = struct.unpack(next_format, data[:next_size])
        data = data[next_size:]

        pack.operator_location_type = types & 0x03
        pack.classification_type = (types & 0x1C) >> 2
        pack.latitude = lat
        pack.longitude = lng
        pack.area_count = a_count
        pack.area_radius = a_radius
        pack.area_ceiling = a_ceil
        pack.area_floor = a_floor
        pack.category = (cat & 0xF0) >> 4
        pack.class_value = cat & 0x0F
        pack.altitude_geodetic = alt_geo
        pack.system_timestamp = ts

        # Do some calculation to convert raw values
        pack.latitude = LAT_LONG_MULTIPLIER * pack.latitude
        pack.longitude = LAT_LONG_MULTIPLIER * pack.longitude
        pack.area_radius = pack.area_radius * 10
        pack.area_ceiling = RemoteID_System.calc_altitude(pack.area_ceiling)
        pack.area_floor = RemoteID_System.calc_altitude(pack.area_floor)
        pack.altitude_geodetic = RemoteID_System.calc_altitude(pack.altitude_geodetic)

        return pack

    def pack(self):
        raw_latitude = int(self.latitude / LAT_LONG_MULTIPLIER)
        raw_longitude = int(self.longitude / LAT_LONG_MULTIPLIER)
        raw_area_radius = int(self.area_radius / 10)
        raw_area_ceiling = RemoteID_System.calc_altitude_raw(self.area_ceiling)
        raw_area_floor = RemoteID_System.calc_altitude_raw(self.area_floor)
        raw_altitude_geodetic = RemoteID_System.calc_altitude_raw(self.altitude_geodetic)

        classification_type = (self.classification_type << 2) & 0x1C
        operator_location_type = self.operator_location_type & 0x03
        types = classification_type | operator_location_type

        category = (self.category << 4) & 0xF0
        class_value = self.class_value & 0x0F
        cat = category | class_value

        pack1 = struct.pack("<BiiHBHHBHI", types, raw_latitude, raw_longitude, self.area_count, raw_area_radius, raw_area_ceiling, raw_area_floor, cat, raw_altitude_geodetic, self.system_timestamp)

        return pack1 + (b"\0" * 1)
    
    @staticmethod
    def calc_altitude(value) -> float:
        return value / 2 - 1000

    @staticmethod
    def calc_altitude_raw(value) -> float:
        return int((value + 1000) * 2)

    def __str__(self) -> str:
        return f"RemoteID_System: latitude={self.latitude} longitude={self.longitude} operator_location_type={self.get_key_from_value(System_Operator_Location_Type, self.operator_location_type)} classification_type={self.get_key_from_value(System_Classification_Type, self.classification_type)} area_count={self.area_count} area_radius={self.area_radius} area_ceiling={self.area_ceiling} area_floor={self.area_floor} category={self.get_key_from_value(System_Category, self.category)} class_value={self.get_key_from_value(System_Class, self.class_value)} altitude_geodetic={self.altitude_geodetic} system_timestamp={self.system_timestamp}"
