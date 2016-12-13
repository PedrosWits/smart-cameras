from smartcameras.vehicle import NormalVehicle, vehicleFromJson
import random
import numpy as np
import math

def test_vehicle():
    random.seed(1337)
    np.random.seed(1337)
    truck = NormalVehicle(30)
    assert truck.plate == "QN35 EVJ"
    assert truck.type == "TRUCK"
    assert truck.speed > 0

def test_json():
    vehicle = NormalVehicle()
    vehicle_json = vehicle.toJson()
    vehicle2 = vehicleFromJson(vehicle_json)

    assert type(vehicle) == type(vehicle2)
    assert vehicle.plate == vehicle2.plate
    assert vehicle.speed == vehicle2.speed
    assert vehicle.type == vehicle2.type
