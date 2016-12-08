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
        self.isActivated = False
        self.speedLimit = None
        self.rate = None

    def relocate(self, street, city = None):
        self.street = street
        if(city is not None):
            self.city = city

    def activate(self, speedLimit, rate):
        if(self.isActivated is True):
            raise EnvironmentError('Speed camera is already active: deactivate first.')
        self.speedLimit = speedLimit
        self.rate = rate
        self.datetime = datetime.datetime.now()
        self.isActivated = True
        # Inform Azure of activated camera
        self.__notifyAzureOfSelf()
        # Event representing the passing of the next vehicle
        self.nextVehicle = threading.Event()
        # Loop until deactivate is called
        # (preferably from a separate thread/process!!!!)
        while self.isActivated:
            nextArrival = self.__genNextArrival()
            self.nextVehicle.wait(timeout=nextArrival)
            # Vehicle has passed - Create new vehicle
            self.__onObservedVehicle()
        # End of Loop

    #
    def deactivate(self):
        self.isActivated = False
        self.nextVehicle.set()

    ## Helping/Private methods

    def __genNextArrival(self):
        if(self.rate is None):
            raise ValueError("Rate is undefined")        
        return np.random.exponential(1./self.rate)

    def __notifyAzureOfSelf(self):
        print "Notifying Azure of Self"
        return False

    def __notifyAzureOfVehicle(self, vehicle):
        print "Sending vehicle detection to Azure"
        return False

    def __onObservedVehicle(self):
        print "Woooooooooooooo -  A new vehicle just passed by"
        return False
