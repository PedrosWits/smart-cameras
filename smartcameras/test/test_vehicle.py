import smartcameras.vehicle as vehicle
import random
import numpy as np
import math

def test_vehicle():
    random.seed(1337)
    np.random.seed(1337)
    truck = vehicle.NormalVehicle(30)
    assert truck.plate == "QN35 EVJ"
    assert truck.type == "TRUCK"
    assert math.floor(truck.speed) == 27
