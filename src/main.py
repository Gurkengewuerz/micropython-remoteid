from remoteid.manager import RemoteIDManager, RemoteIDManager_Mode
from remoteid.messages.basicid import RemoteID_BasicID, BasicID_ID_Type, BasicID_UA_Type
from remoteid.messages.selfid import RemoteID_SelfID, SelfID_Description_Type
from remoteid.messages.operatorid import RemoteID_OperatorID, OperatorID_Type
from remoteid.messages.location import RemoteID_Location, Location_Status, Location_Height_Type
from remoteid.messages.system import RemoteID_System, System_Category, System_Class, System_Classification_Type, System_Operator_Location_Type

import time

manager = RemoteIDManager()

if __name__ == "__main__":
    start = time.ticks_ms()

    #print("Listening")
    #manager.set_mode(RemoteIDManager_Mode["LISTEN"])

    print("Sending")
    manager.set_mode(RemoteIDManager_Mode["SEND"])

    msg = RemoteID_BasicID()
    msg.ua_type = BasicID_UA_Type["ROCKET"]
    msg.id_type = BasicID_ID_Type["SERIAL_NUMBER"]
    msg.uas_id = "123-abc"
    manager.queue_add(msg)

    msg = RemoteID_SelfID()
    msg.description_type = SelfID_Description_Type["TEXT"]
    msg.operation_description = "THIS IS A TEST!"
    manager.queue_add(msg)

    msg = RemoteID_OperatorID()
    msg.operator_type = OperatorID_Type["CAA"]
    msg.operator_id = "somebody"
    manager.queue_add(msg)

    msg = RemoteID_System()
    msg.operator_location_type = System_Operator_Location_Type["FIXED"]
    msg.classification_type = System_Classification_Type["EU"]
    msg.latitude = 51.549999
    msg.longitude = 7.216667
    msg.area_count = 0
    msg.area_radius = 0
    msg.area_ceiling = 0
    msg.area_floor = 0
    msg.category = System_Category["OPEN"]
    msg.class_value = System_Class["CLASS_4"]
    msg.altitude_geodetic = 1
    msg.system_timestamp = 0
    manager.queue_add(msg)

    msg = RemoteID_Location()
    msg.status = Location_Status["ON_GROUND"]
    msg.height_type = Location_Height_Type["ABOVE_START"]
    msg.direction = 167
    msg.speed_hori = 153.1
    msg.speed_vert = 0
    msg.latitude = 51.549999
    msg.longitude = 7.216667
    msg.altitude_pressure = 2.1
    msg.altitude_geodetic = 2.1
    msg.height = 2.1
    msg.timestamp = 0
    msg.accuracy_time = 0
    msg.accuracy_horizontal = 12
    msg.accuracy_vertical = 6
    msg.accuracy_baro = 6
    msg.accuracy_speed = 1
    manager.queue_add(msg)

    while time.ticks_ms() - start < 10 * 1000:
        manager.send_bluetooth()
        time.sleep(0.01)
    
    manager.set_mode(None)
    print("Stopped")

