import numpy as np
import string
import random

VehicleType = ["CAR", "TRUCK", "MOTORCYCLE"]

class NormalVehicle(object):

    def __init__(self, maximumSpeed = 50):
        if(maximumSpeed < 30):
            raise ValueError('Maximum speed should be at least 30 km per hour')
        # Uniformly sample from from upper case letters and numbers
        self.plate = random.choice(string.ascii_uppercase) + \
                     random.choice(string.ascii_uppercase) + \
                     random.choice(string.digits) + \
                     random.choice(string.digits) + \
                     " " + \
                     random.choice(string.ascii_uppercase) + \
                     random.choice(string.ascii_uppercase) + \
                     random.choice(string.ascii_uppercase)
        # Uniformly sample from vehicle type
        index = np.random.randint(0, len(VehicleType))
        self.type = VehicleType[index]
        # Sample vehicle speed from a normal distribution
        #  from which mu and sigma are obtained from the
        #  following system of equations:
        #       mu + sigma = maximumSpeed
        #       mu - 3sgima = 10
        sigma = (maximumSpeed - 10) / 4
        mu = maximumSpeed - sigma
        self.speed = np.random.normal(mu, sigma)

    def dump(self):
        print "License plate = " , self.plate
        print "Type = " , self.type
        print "Speed = " , self.speed
