import uuid
import datetime
import time
import numpy as np
import threading
import vehicle
import azurehook
import json

class SpeedCamera(object):
    TOPIC = "SpeedCamera"
    EVENT_ACTIVATION = "Camera_Activated"
    EVENT_DEACTIVATION = "Camera_Deactivated"
    EVENT_VEHICLE = "Vehicle_Detected"

    def __init__(self, street, city, cloudhook = None, name = None):
        self.id = str(uuid.uuid4())
        self.street = street
        self.city = city
        self.isActive = False
        self.speedLimit = None
        self.rate = None
        if cloudhook is None:
            self.cloudhook = azurehook.AzureHook()
            self.cloudhook.createTopic(self.TOPIC)
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
        self.datetime = datetime.datetime.now()
        self.__notifyCloudOfSelf()

    # Preferably called from a separate thread
    def deactivate(self):
        if not self.isActive:
            raise ValueError("Camera is not active")
        self.isActive = False
        self.nextVehicle.set()

    def toDict(self):
        return {"id"         : self.id,
                "street"     : self.street,
                "city"       : self.city,
                "rate"       : self.rate,
                "speedLimit" : self.speedLimit,
                "isActive"   : str(self.isActive),
                "timestamp"  : datetimeToTimestamp(self.datetime)}

    def toJson(self):
        return json.dumps(self.toDict(), indent = 4, sort_keys = True)

    ## Helping/Private methods
    ################################################
    def __genNextArrival(self):
        if(self.rate is None):
            raise ValueError("Rate is undefined")
        return np.random.exponential(1./self.rate)

    def __notifyCloudOfSelf(self):
        dic = {}
        if self.isActive:
            dic['event'] = self.EVENT_ACTIVATION
        else:
            dic['event'] = self.EVENT_DEACTIVATION
        dic['camera'] = self.toDict()
        json_string = json.dumps(dic, indent = 4, sort_keys = False)
        self.cloudhook.publish(self.TOPIC, json_string)

    def __notifyCloudOfVehicle(self, vehicle):
        dic = {}
        dic['event'] = self.EVENT_VEHICLE
        dic['vehicle'] = vehicle.toDict()
        dic['camera'] = self.toDict()
        json_string = json.dumps(dic, indent = 4, sort_keys = True)
        self.cloudhook.publish(self.TOPIC, json_string)

    def __onObservedVehicle(self):
        aVehicle = vehicle.NormalVehicle(self.speedLimit)
        self.__notifyCloudOfVehicle(aVehicle)


def datetimeToTimestamp(dt):
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

## Global "factory" functions
def activateInNewThread(camera, speedLimit, rate, daemon = True):
    thread = threading.Thread(target=camera.activate, args=(speedLimit, rate))
    thread.daemon = daemon
    thread.start()
    return thread

# def main():
#     parser = argparse.ArgumentParser(
#         description='Launch a speed camera')
#     parser.add_argument('action',
#                         metavar="<action>",
#                         choices=['start', 'shutdown', 'status', 'camera'],
#                         help='%(choices)s')
#     thread = threading.Thread(target=camera.activate, args=(speedLimit, rate))
#     thread.start()
#     return thread.isAlive
#
# if __name__ == "__main__":
#     main()
