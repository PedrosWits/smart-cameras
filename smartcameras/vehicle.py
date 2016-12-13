import numpy as np
import string
import random
import json

VehicleType = ["CAR", "TRUCK", "MOTORCYCLE"]

class NormalVehicle(object):

    def __init__(self, maximumSpeed = 50):
        if(maximumSpeed < 30):
            raise ValueError('Maximum speed should be at least 30 km per hour')
        # Uniformly sample from from upper case letters and numbers
        self.plate = genLetter() + genLetter() + \
                     genNumber() + genNumber() + " " + \
                     genLetter() + genLetter() + genLetter()
        # Uniformly sample from vehicle type
        index = np.random.randint(0, len(VehicleType))
        self.type = VehicleType[index]
        # Sample vehicle speed from a normal distribution
        #  centered at (maximumSpeed + sigma) with sigma = 1/5 of maximumSpeed
        sigma = maximumSpeed / 5
        mu = maximumSpeed + sigma
        self.speed = np.random.normal(mu, sigma)
        self.isSpeeding = self.speed > maximumSpeed
        self.isPriority = (1.10 * self.speed) > maximumSpeed

    def dump(self):
        print("")
        print "License plate =" , self.plate
        print "Type =" , self.type
        print "Speed =" , self.speed
        print "Is speeding = ", self.isSpeeding
        print "Is priority = ", self.isPriority


    def toDict(self):
        return {"plate" : self.plate,
                "type"  : self.type,
                "speed" : self.speed,
                "isSpeeding" : self.isSpeeding,
                "isPriority" : self.isPriority}

    def toJson(self):
        return json.dumps(self.toDict(), indent = 4, sort_keys = False)

def vehicleFromJson(json_string):
    return json.loads(json_string, object_hook=asVehicle)

def asVehicle(dic):
    vehicle = NormalVehicle()
    vehicle.__dict__.update(dic)
    return vehicle

def genNumber():
    return random.choice(string.digits)

def genLetter():
    return random.choice(string.ascii_uppercase)
