import uuid
import datetime
import time
import numpy as np
import threading

class SpeedCamera(object):

    def __init__(self, street, city):
        self.id = uuid.uuid4()
        self.street = street
        self.city = city

    def relocate(self, street, city):
        self.stree = street
        selt.city = city

    def activate(self, rate, speedLimit):
        self.speedLimit = speedLimit
        self.rate = rate
        self.datetime = datetime.datetime.now()
        self.isActivated = threading.Event()
        # Inform Azure
        self.__notifyAzureOfSelf()
        # Loop
        while self.isActivated.wait(timeout=self.__next_arrival(rate)):
            # Vehicle has passed - Create new vehicle
            self.__onObservedVehicle()

    def deactivate(self):
        self.isActivated = False

    def __next_arrival(self, rate):
        return np.random.poisson(rate, 1)

    def __notifyAzureOfSelf(self):

    def __notifyAzureOfVehicle(self, vehicle):

    def __onObservedVehicle(self)
