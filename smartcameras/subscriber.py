from abc import ABCMeta, abstractmethod
import azurehook
import threading
import json
import math

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
