from abc import ABCMeta, abstractmethod
from azure.servicebus import Rule
from speedcamera import SpeedCamera
import azurehook
import threading
import json
import math
import time
import Queue
import random

################################################################################
################################################################################
#
#      A Generic Class responsible for handling data received
#     through an Azure subscription
#
################################################################################
################################################################################
class AzureSubscriber(object):
    __metaclass__ = ABCMeta

    def __init__(self, topicName, subscriptionName, ruleName = None, rule = None):
        self.azure = azurehook.AzureHook()
        self.topic = topicName
        self.subscription = subscriptionName
        self.ruleName = ruleName
        self.rule = rule
        self.isActive = False

    def activate(self, timeout = 2):
        self.azure.subscribe(self.topic, self.subscription)
        # Create rule if given
        if self.ruleName is not None and self.rule is not None:
            self.azure.serviceBus.create_rule(self.topic, self.subscription, self.ruleName, self.rule)
            self.azure.serviceBus.delete_rule(self.topic, self.subscription, '$Default')
        self.isActive = True
        self.nextCheck = threading.Event()
        retries = 0
        while self.isActive:
            message = self.azure.getMessage(
                            self.topic,
                            self.subscription,
                            timeout=timeout)
            # print(message.body)
            # If no message was retrieved - try again later with exponential backoff
            if message is None or message.body is None:
                retries += 1
            else:
                body = json.loads(message.body)
                self.onNewMessage(body)
                retries = 0
            # Calculate exponential backoff and sleep (may be woken up by terminate)
            self.nextCheck.wait(self.__nextTimeout(retries))

    def terminate(self):
        self.isActive = False
        self.nextCheck.set()
        self.onTerminate()

    def onTerminate(self):
        pass

    # Initially Amortized exponential backoff:
    # Given by the formula: timeout(seconds) = (2^ntries / 10)
    def __nextTimeout(self, ntries, maxNtries = 12):
        # Define maximum timeout
        if(ntries > maxNtries):
            ntries = maxNtries
        # if ntries == 0 -> timeout = 0.100 ms
        # if ntries == 12 -> timeout = 6.66 min
        return math.pow(2, ntries) / 10.

    @abstractmethod
    def onNewMessage(self, dic):
        pass


################################################################################
################################################################################
#
#     Class responsible for vehicle checks
#
################################################################################
################################################################################

class VehicleInspector(AzureSubscriber):

    def __init__(self, queueSize = 0):
        rule = Rule()
        rule.filter_type = 'SqlFilter'
        rule.filter_expression = "event = '%s'" % (SpeedCamera.EVENT_VEHICLE)
        # Call super class constructor
        AzureSubscriber.__init__(self, SpeedCamera.TOPIC, "VehicleInspector",
                                 "VehicleInspectorRule", rule)
        # Thread runs isVehicleStolen which processes items from queue
        # (blocks until one is available)
        processingThread = threading.Thread(target=self.vehicleProcessing)
        # If parent thread exists this one exits too
        processingThread.daemon = True
        processingThread.start()

    def onNewMessage(self, dic):
        plate = dic['vehicle']['plate']
        self.queue.put(plate, block = True, timeout = 10)
        # print("Size of queue (after put) =  %d" % self.queue.qsize())

    # This will be killed when parent thread is killed
    def vehicleProcessing(self):
        # Instantiate queue
        self.queue = Queue.Queue()
        print("")
        print("Vehicle processing started (queue size =  %d)" % self.queue.qsize())
        while True:
            plate = self.queue.get(block = True, timeout = None)
            isStolen = self.isVehicleStolen(plate)
            if isStolen:
                print "Vehicle with plate '%s' is stolen!!!" % plate
            else:
                print "Vehicle with plate '%s' is NOT stolen." % plate

    # Should be called from a separate thread
    def isVehicleStolen(self, plate, sleepFor = 5):
        print ""
        print "Processing vehicle with plate: '%s'" % plate
        time.sleep(sleepFor)
        return random.random() > 0.95

    def onTerminate(self):
        print "Killed"
        print ""
        print("Size of queue =  %d" % self.queue.qsize())
