from .interface import RemoteID_Message, SPEED_VERTICAL_MULTIPLIER, LAT_LONG_MULTIPLIER
import struct

Location_Status = {
    "NONE": 0,
    "ON_GROUND": 1,
    "IN_AIR": 2,
    "EMERGENCY": 3,
}

Location_Height_Type = {
    "ABOVE_START": 0,
    "AGL": 1
}


class RemoteID_Location(RemoteID_Message):

    def __init__(self) -> None:
        # See DIN EN 4709-002 for specific values i.e. for the accuracy
        self.status = Location_Status["NONE"]
        self.height_type = Location_Height_Type["AGL"]
        self.ew_direction = 0
        self.speed_mult = 0
        self.direction = 0
        self.speed_hori = 0
        self.speed_vert = 0
        self.latitude = 51.549999
        self.longitude = 7.216667
        self.altitude_pressure = 10.5
        self.altitude_geodetic = 10.5
        self.height = 10.5
        self.timestamp = 0
        self.accuracy_time = 0
        self.accuracy_horizontal = 0
        self.accuracy_vertical = 0
        self.accuracy_baro = 0
        self.accuracy_speed = 0

    @staticmethod
    def parse(data) -> "RemoteID_Location":
        pack = RemoteID_Location()

        b = data[0]
        pack.status = (b & 0xF0) >> 4
        pack.height_type = (b & 0x04) >> 2
        pack.ew_direction = (b & 0x02) >> 1
        pack.speed_mult = b & 0x01

        pack.direction = data[1]
        pack.speed_hori = data[2]
        pack.speed_vert = data[3]

        data = data[4:]

        next_format = "<iihhh"
        next_size = struct.calcsize(next_format)
        lat, lng, altPres, altGeo, height = struct.unpack(next_format, data[:next_size])
        data = data[next_size:]

        pack.latitude = lat
        pack.longitude = lng

        pack.altitude_pressure = altPres
        pack.altitude_geodetic = altGeo
        pack.height = height

        next_format = "<BBHB"
        next_size = struct.calcsize(next_format)
        hori_vert_acc, speed_baro_acc, ts, time_acc = struct.unpack(next_format, data[:next_size])
        data = data[next_size:]

        pack.accuracy_horizontal = hori_vert_acc & 0x0F
        pack.accuracy_vertical = (hori_vert_acc & 0xF0) >> 4
        pack.accuracy_baro = (speed_baro_acc & 0xF0) >> 4
        pack.accuracy_speed = speed_baro_acc & 0x0F
        pack.timestamp = ts
        pack.accuracy_time = time_acc

        # Do some calculation to convert raw values
        pack.direction = RemoteID_Location.calc_direction(pack.direction, pack.ew_direction)
        pack.speed_hori = RemoteID_Location.calc_speed(pack.speed_hori, pack.speed_mult)
        pack.speed_vert = SPEED_VERTICAL_MULTIPLIER * pack.speed_vert
        pack.latitude = LAT_LONG_MULTIPLIER * pack.latitude
        pack.longitude = LAT_LONG_MULTIPLIER * pack.longitude
        pack.altitude_pressure = RemoteID_Location.calc_altitude(pack.altitude_pressure)
        pack.altitude_geodetic = RemoteID_Location.calc_altitude(pack.altitude_geodetic)
        pack.height = RemoteID_Location.calc_altitude(pack.height)
        pack.accuracy_time = pack.accuracy_time * 0.1

        return pack

    def pack(self):
        if self.direction > 179:
            self.ew_direction = 1
        else:
            self.ew_direction = 0

        if self.speed_hori <= 255 * 0.25:
            self.speed_mult = 0
        else:
            self.speed_mult = 1

        raw_speed_vert = int(self.speed_vert / SPEED_VERTICAL_MULTIPLIER)
        raw_latitude = int(self.latitude / LAT_LONG_MULTIPLIER)
        raw_longitude = int(self.longitude / LAT_LONG_MULTIPLIER)
        raw_accuracy_time = int(self.accuracy_time / 0.1)
        raw_direction = RemoteID_Location.calc_direction_raw(self.direction, self.ew_direction)
        raw_speed_hori = RemoteID_Location.calc_speed_raw(self.speed_hori, self.speed_mult)
        raw_altitude_pressure = RemoteID_Location.calc_altitude_raw(self.altitude_pressure)
        raw_altitude_geodetic = RemoteID_Location.calc_altitude_raw(self.altitude_geodetic)
        raw_height = RemoteID_Location.calc_altitude_raw(self.height)

        a = (self.status << 4) & 0xF0
        b = (self.height_type << 2) & 0x04
        c = (self.ew_direction << 1) & 0x02
        d = self.speed_mult & 0x01
        first = ((a | b | c | d) & 0xFF).to_bytes(1, "little")

        pack1 = first + (raw_direction & 0xFF).to_bytes(1, "little") + (raw_speed_hori & 0xFF).to_bytes(1, "little") + (raw_speed_vert & 0xFF).to_bytes(1, "little")
        pack2 = struct.pack("<iihhh", raw_latitude, raw_longitude, raw_altitude_pressure, raw_altitude_geodetic, raw_height)

        accuracy_vertical = (self.accuracy_vertical << 4) & 0xF0
        accuracy_horizontal = self.accuracy_horizontal & 0x0F
        e = accuracy_vertical | accuracy_horizontal
        accuracy_baro = (self.accuracy_baro << 4) & 0xF0
        accuracy_speed = self.accuracy_speed & 0x0F
        f = accuracy_baro | accuracy_speed

        pack3 = struct.pack("<BBHB", e, f, self.timestamp, raw_accuracy_time & 0x07)

        return pack1 + pack2 + pack3 + (b"\0" * 1)

    @staticmethod
    def calc_speed(value, mult) -> float:
        if mult == 0:
            return value * 0.25
        return (value * 0.75) + (255 * 0.25)

    @staticmethod
    def calc_speed_raw(value, mult) -> float:
        if mult == 0:
            return int(value / 0.25)
        return int((value - (255 * 0.25)) / 0.75)

    @staticmethod
    def calc_direction(value, ew) -> float:
        if ew == 0:
            return value
        return value + 180

    @staticmethod
    def calc_direction_raw(value, ew) -> float:
        if ew == 0:
            return value
        return value - 180

    @staticmethod
    def calc_altitude(value) -> float:
        return value / 2 - 1000

    @staticmethod
    def calc_altitude_raw(value) -> float:
        return int((value + 1000) * 2)

    def __str__(self) -> str:
        return f"RemoteID_Location: latitude={self.latitude} longitude={self.longitude} status={self.get_key_from_value(Location_Status, self.status)} height={self.height} height_type={self.get_key_from_value(Location_Height_Type, self.height_type)} altitude_pressure={self.altitude_pressure} altitude_geodetic={self.altitude_geodetic} direction={self.direction} speed_hori={self.speed_hori} speed_vert={self.speed_vert} speed_mult={self.speed_mult} ew_direction={self.ew_direction} timestamp={self.timestamp} accuracy_time={self.accuracy_time} accuracy_horizontal={self.accuracy_horizontal} accuracy_vertical={self.accuracy_vertical} accuracy_baro={self.accuracy_baro} accuracy_speed={self.accuracy_speed}"
