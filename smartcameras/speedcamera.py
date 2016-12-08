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
        self.street = street
        selt.city = city

    def activate(self, speedLimit, rate):
        if(self.isActivated is None or self.isActivated is True):
            raise EnvironmentError('Speed camera is already active. Deactivate first.')
        self.speedLimit = speedLimit
        self.rate = rate
        self.datetime = datetime.datetime.now()
        self.isActivated = True
        self.nextVehicle = threading.Event()
        # Inform Azure
        self.__notifyAzureOfSelf()
        # Loop
        while self.isActivated:
            nextArrival = self.__genNextArrival(rate)
            nextVehicle.wait(timeout=nextArrival):
            # Vehicle has passed - Create new vehicle
            self.__onObservedVehicle()
        # End of Loop

    def deactivate(self):
        self.isActivated = False
        self.nextVehicle.set()

    ## Helping/Private methods

    def __genNextArrival(self, rate):
        return np.random.poisson(rate, 1)

    def __notifyAzureOfSelf(self):
        print "Notifying Azure of Self"
        return False

    def __notifyAzureOfVehicle(self, vehicle):
        print "Sending vehicle detection to Azure"
        return False

    def __onObservedVehicle(self):
        print "Woooooooooooooo -  A new vehicle just passed by"
        return False
