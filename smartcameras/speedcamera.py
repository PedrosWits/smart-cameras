import uuid
import datetime
import time
import numpy as np
import threading
import vehicle
import azurehook

class SpeedCamera(object):

    def __init__(self, street, city, cloudhook = None, name = None):
        self.id = uuid.uuid4()
        self.street = street
        self.city = city
        self.isActive = False
        self.speedLimit = None
        self.rate = None
        if cloudhook is None:
            self.cloudhook = azurehook.AzureHook()
        if name is not None:
            self.name = name

    def relocate(self, street, city = None):
        self.street = street
        if(city is not None):
            self.city = city

    # Most commonly executes on its own thread
    def activate(self, speedLimit, rate):
        if(self.isActive is True):
            raise EnvironmentError('Speed camera is already active: deactivate first.')
        self.speedLimit = speedLimit
        self.rate = rate
        self.datetime = datetime.datetime.now()
        self.isActive = True
        # Inform Azure of activated camera
        self.__notifyCloudOfSelf()
        # Event representing the passing of the next vehicle
        self.nextVehicle = threading.Event()
        # Loop until deactivate is called
        # (preferably from a separate thread/process!!!!)
        while self.isActive:
            nextArrival = self.__genNextArrival()
            self.nextVehicle.wait(timeout=nextArrival)
            # Vehicle has passed - Create new vehicle
            self.__onObservedVehicle()
        # End of Loop

    # Preferably called from a separate thread
    def deactivate(self):
        self.isActive = False
        self.nextVehicle.set()

    ## Helping/Private methods
    ################################################
    def __genNextArrival(self):
        if(self.rate is None):
            raise ValueError("Rate is undefined")
        return np.random.exponential(1./self.rate)

    def __notifyCloudOfSelf(self):

        print "Notifying Azure of Self"
        return False

    def __notifyCloudOfVehicle(self, vehicle):
        print "Sending vehicle detection to Azure"
        return False

    def __onObservedVehicle(self):
        # print "Woooooooooooooo -  A new vehicle just passed by"
        aVehicle = vehicle.NormalVehicle(self.speedLimit)
        self.__notifyCloudOfVehicle(aVehicle)


# def main():
#     parser = argparse.ArgumentParser(
#         description='Launch a speed camera')
#     parser.add_argument('action',
#                         metavar="<action>",
#                         choices=['start', 'shutdown', 'status', 'camera'],
#                         help='%(choices)s')
#
# if __name__ == "__main__":
#     main()
