import numpy as np
import string
import random

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
        #  centered at maximumSpeed with sigma = 1/5 of maximumSpeed
        sigma = maximumSpeed / 5
        mu = maximumSpeed
        self.speed = np.random.normal(mu, sigma)

    def dump(self):
        print "License plate =" , self.plate
        print "Type =" , self.type
        print "Speed =" , self.speed

def genNumber():
    return random.choice(string.digits)

def genLetter():
    return random.choice(string.ascii_uppercase)
